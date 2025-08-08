import requests
import os
import re
from typing import Optional
from urllib.parse import urlparse, parse_qs
import PyPDF2
import io
from .resume_converter import ResumeConverter

class ResumeExtractor:
    """Handles extraction of resume content from various sources"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.converter = ResumeConverter()
    
    def extract_content(self, resume_url: str) -> Optional[str]:
        """
        Extract content from resume URL
        Supports: Google Drive, direct URLs, local files
        """
        if not resume_url:
            return None
            
        try:
            if resume_url.startswith('http'):
                return self._extract_from_url(resume_url)
            else:
                return self._extract_from_file(resume_url)
        except Exception as e:
            print(f"Error extracting resume content from {resume_url}: {e}")
            return None
    
    def _extract_from_url(self, url: str) -> Optional[str]:
        """Extract content from URL (Google Drive or direct)"""
        if 'drive.google.com' in url:
            return self._extract_from_google_drive(url)
        else:
            return self._extract_from_direct_url(url)
    
    def _extract_from_google_drive(self, url: str) -> Optional[str]:
        """Extract content from Google Drive URL"""
        try:
            # Convert Google Drive URL to direct download URL
            file_id = self._extract_file_id_from_gdrive_url(url)
            if not file_id:
                print(f"Could not extract file ID from Google Drive URL: {url}")
                return None
            
            # Create direct download URL
            direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            # Download the file
            response = requests.get(direct_url, timeout=self.timeout)
            if response.status_code != 200:
                print(f"Failed to download from Google Drive: {response.status_code}")
                return None
            
            # Check if it's a PDF
            content_type = response.headers.get('content-type', '')
            print(f"Content-Type: {content_type}")
            print(f"Response size: {len(response.content)} bytes")
            
            # Check if content starts with PDF signature
            if response.content.startswith(b'%PDF-'):
                print("Detected PDF by signature")
                return self._extract_text_from_pdf(response.content)
            elif 'pdf' in content_type.lower():
                print("Detected PDF by content-type")
                return self._extract_text_from_pdf(response.content)
            else:
                print("Non-PDF file detected, extracting text directly...")
                # Extract text directly from the file
                text_content = self.converter.download_and_extract_text(url)
                if text_content:
                    return text_content
                else:
                    print("Failed to extract text from file")
                    return response.text  # Fallback to original content
                
        except Exception as e:
            print(f"Error extracting from Google Drive: {e}")
            return None
    
    def _extract_file_id_from_gdrive_url(self, url: str) -> Optional[str]:
        """Extract file ID from Google Drive URL"""
        # Handle different Google Drive URL formats
        patterns = [
            r'/file/d/([a-zA-Z0-9_-]+)',  # /file/d/FILE_ID
            r'id=([a-zA-Z0-9_-]+)',       # ?id=FILE_ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_from_direct_url(self, url: str) -> Optional[str]:
        """Extract content from direct URL"""
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code != 200:
                return None
            
            content_type = response.headers.get('content-type', '')
            if 'pdf' in content_type.lower() or response.content.startswith(b'%PDF-'):
                return self._extract_text_from_pdf(response.content)
            else:
                print("Non-PDF file detected, extracting text directly...")
                # Extract text directly from the file
                text_content = self.converter.download_and_extract_text(url)
                if text_content:
                    return text_content
                else:
                    print("Failed to extract text from file")
                    return response.text  # Fallback to original content
                
        except Exception as e:
            print(f"Error extracting from direct URL: {e}")
            return None
    
    def _extract_text_from_pdf(self, pdf_content: bytes) -> Optional[str]:
        """Extract text from PDF content"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            total_pages = len(pdf_reader.pages)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        # Clean up the text - remove excessive whitespace
                        cleaned_page = ' '.join(page_text.split())
                        text += cleaned_page + "\n"
                        print(f"Page {page_num}: Extracted {len(cleaned_page)} characters")
                    else:
                        print(f"Page {page_num}: No text extracted - trying OCR...")
                        # Try OCR for image-based PDFs
                        ocr_text = self._extract_text_with_ocr(pdf_content, page_num)
                        if ocr_text:
                            text += ocr_text + "\n"
                            print(f"Page {page_num}: OCR extracted {len(ocr_text)} characters")
                        else:
                            print(f"Page {page_num}: OCR also failed")
                except Exception as e:
                    print(f"Error extracting text from page {page_num}: {e}")
                    # Try OCR as fallback
                    print(f"Page {page_num}: Trying OCR as fallback...")
                    ocr_text = self._extract_text_with_ocr(pdf_content, page_num)
                    if ocr_text:
                        text += ocr_text + "\n"
                        print(f"Page {page_num}: OCR fallback extracted {len(ocr_text)} characters")
                    continue
            
            # Clean up the final text
            cleaned_text = text.strip()
            
            print(f"Total extracted: {len(cleaned_text)} characters from {total_pages} pages")
            
            # Check if the content is too large (likely corrupted or contains binary data)
            if len(cleaned_text) > 100000:  # More than 100K characters is suspicious
                print(f"Warning: Extracted content is very large ({len(cleaned_text)} chars). Likely contains binary data.")
                # Try to clean it up by taking only the first reasonable portion
                lines = cleaned_text.split('\n')
                cleaned_lines = []
                for line in lines[:200]:  # Take first 200 lines
                    if len(line.strip()) < 1000:  # Skip extremely long lines
                        cleaned_lines.append(line.strip())
                cleaned_text = '\n'.join(cleaned_lines)
                print(f"Cleaned content: {len(cleaned_text)} characters")
            
            # If we got very little text, try OCR on the entire PDF
            if len(cleaned_text) < 50:
                print(f"Warning: Very little text extracted ({len(cleaned_text)} chars). Trying full OCR...")
                full_ocr_text = self._extract_text_with_ocr(pdf_content)
                if full_ocr_text and len(full_ocr_text) > 50:
                    print(f"OCR extracted {len(full_ocr_text)} characters from image-based PDF")
                    return full_ocr_text
                else:
                    print("OCR also failed - using fallback content")
                    return self._create_fallback_content(pdf_reader, pdf_content, total_pages)
            
            # Return whatever text we have, even if it's limited
            return cleaned_text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            # Try OCR as last resort
            print("Trying OCR as last resort...")
            ocr_text = self._extract_text_with_ocr(pdf_content)
            if ocr_text:
                return ocr_text
            else:
                return f"PDF Resume - Error during text extraction: {str(e)}. File size: {len(pdf_content)} bytes."
    
    def _extract_text_with_ocr(self, pdf_content: bytes, page_num: int = None) -> Optional[str]:
        """Extract text from PDF using Mistral OCR API (for image-based PDFs)"""
        try:
            from pdf2image import convert_from_bytes
            import requests
            import base64
            from ..utils.config import MISTRAL_OCR_API_KEY
            
            if not MISTRAL_OCR_API_KEY:
                print("Mistral OCR API key not found in environment variables")
                return None
            
            # Convert PDF pages to images
            if page_num:
                # Convert specific page
                images = convert_from_bytes(pdf_content, first_page=page_num, last_page=page_num)
            else:
                # Convert all pages
                images = convert_from_bytes(pdf_content)
            
            text = ""
            for i, image in enumerate(images, 1):
                try:
                    # Convert image to base64
                    import io
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                    
                    # Call Mistral OCR API
                    headers = {
                        'Authorization': f'Bearer {MISTRAL_OCR_API_KEY}',
                        'Content-Type': 'application/json'
                    }
                    
                    payload = {
                        'image': img_base64,
                        'model': 'mistral-large-latest'  # or your preferred model
                    }
                    
                    response = requests.post(
                        'https://api.mistral.ai/v1/chat/completions',
                        headers=headers,
                        json={
                            'model': 'mistral-large-latest',
                            'messages': [
                                {
                                    'role': 'user',
                                    'content': [
                                        {
                                            'type': 'text',
                                            'text': 'Extract all text from this image. Return only the extracted text without any additional formatting or explanations.'
                                        },
                                        {
                                            'type': 'image_url',
                                            'image_url': {
                                                'url': f'data:image/png;base64,{img_base64}'
                                            }
                                        }
                                    ]
                                }
                            ],
                            'max_tokens': 4000
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        page_text = result['choices'][0]['message']['content'].strip()
                        if page_text:
                            cleaned_page = ' '.join(page_text.split())
                            text += cleaned_page + "\n"
                            print(f"Mistral OCR Page {i}: Extracted {len(cleaned_page)} characters")
                        else:
                            print(f"Mistral OCR Page {i}: No text extracted")
                    else:
                        print(f"Mistral OCR API error on page {i}: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    print(f"Mistral OCR error on page {i}: {e}")
                    continue
            
            return text.strip() if text else None
            
        except ImportError:
            print("pdf2image not available for image conversion")
            return None
        except Exception as e:
            print(f"Error in Mistral OCR extraction: {e}")
            return None
    
    def _create_fallback_content(self, pdf_reader, pdf_content: bytes, total_pages: int) -> str:
        """Create fallback content when text extraction fails"""
        try:
            # Get PDF metadata and structure info
            info = pdf_reader.metadata
            fallback_text = f"PDF Resume with {total_pages} pages. "
            if info:
                title = info.get('/Title', 'Unknown')
                author = info.get('/Author', 'Unknown')
                fallback_text += f"Title: {title}. Author: {author}. "
            fallback_text += f"File size: {len(pdf_content)} bytes. "
            fallback_text += "This PDF appears to contain primarily images or complex formatting that cannot be extracted as text. "
            fallback_text += "The resume content is available but not in text format suitable for AI analysis."
            return fallback_text
        except Exception as meta_e:
            return f"PDF Resume with {total_pages} pages, {len(pdf_content)} bytes. Text extraction limited due to PDF format."
    
    def _extract_from_file(self, file_path: str) -> Optional[str]:
        """Extract content from local file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading local file: {e}")
            return None 
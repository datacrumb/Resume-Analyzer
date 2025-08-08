#!/usr/bin/env python3
"""
Test script to verify OCR functionality for image-based PDFs
"""

import tempfile
import os
from src.sheets.resume_extractor import ResumeExtractor

def test_ocr():
    """Test OCR extraction from image-based PDFs"""
    print("🧪 Testing OCR Functionality")
    print("=" * 50)
    
    extractor = ResumeExtractor()
    
    # Test OCR method directly
    print("\n📝 Testing OCR extraction method...")
    
    # Create a simple test image with text (simulating a scanned document)
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a test image with text
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Add some test text
        test_text = [
            "Test Resume",
            "Name: John Doe",
            "Email: john@example.com",
            "Experience: 5 years in software development",
            "Skills: Python, AI, Machine Learning"
        ]
        
        y_position = 50
        for line in test_text:
            draw.text((50, y_position), line, fill='black', font=font)
            y_position += 30
        
        # Save as PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            img.save(f.name, 'PDF')
            pdf_path = f.name
        
        # Read the PDF content
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        # Test OCR extraction
        ocr_text = extractor._extract_text_with_ocr(pdf_content)
        
        if ocr_text:
            print(f"✅ OCR extraction successful: {len(ocr_text)} characters")
            print(f"📄 Extracted text: {ocr_text[:200]}...")
        else:
            print("❌ OCR extraction failed")
        
        # Clean up
        try:
            os.unlink(pdf_path)
        except:
            pass
            
    except ImportError:
        print("❌ PIL not available for OCR test")
    except Exception as e:
        print(f"❌ OCR test error: {e}")
    
    print("\n✅ OCR tests completed!")

if __name__ == "__main__":
    test_ocr() 
from src.sheets.resume_extractor import ResumeExtractor

def test_pdf_extraction():
    """Test PDF text extraction directly"""
    extractor = ResumeExtractor()
    
    # Test URL from your data
    test_url = "https://drive.google.com/file/d/1X4-8xhrphCaKR4erUr1-2uIpDW8wA1xu/view?usp=drivesdk"
    
    print("Testing PDF extraction...")
    print(f"URL: {test_url}")
    
    content = extractor.extract_content(test_url)
    
    if content:
        print(f"\nExtracted content length: {len(content)} characters")
        print("-" * 100)
        print(content)
        print("-" * 100)
    else:
        print("Failed to extract content")

if __name__ == "__main__":
    test_pdf_extraction() 
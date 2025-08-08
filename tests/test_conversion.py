#!/usr/bin/env python3
"""
Test script to verify PDF conversion functionality
"""

import tempfile
import os
from src.sheets.resume_converter import ResumeConverter

def test_conversion():
    """Test PDF conversion with different file types"""
    print("🧪 Testing PDF Conversion")
    print("=" * 50)
    
    converter = ResumeConverter()
    
    # Test 1: Create a simple TXT file and convert it
    print("\n📝 Testing TXT to PDF conversion...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test Resume Content\n\nName: John Doe\nExperience: 5 years\nSkills: Python, AI")
        txt_path = f.name
    
    try:
        pdf_path = converter.convert_to_pdf(txt_path)
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ TXT to PDF conversion successful: {pdf_path}")
            # Clean up
            os.unlink(pdf_path)
        else:
            print("❌ TXT to PDF conversion failed")
    except Exception as e:
        print(f"❌ TXT to PDF conversion error: {e}")
    finally:
        # Clean up temp file
        try:
            os.unlink(txt_path)
        except:
            pass
    
    # Test 2: Test URL download and conversion
    print("\n🌐 Testing URL download and conversion...")
    # This would test with a real URL, but we'll skip for now
    print("⏭️  URL conversion test skipped (requires internet)")
    
    print("\n✅ Conversion tests completed!")

if __name__ == "__main__":
    test_conversion() 
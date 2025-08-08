from src.sheets.google_sheets import GoogleSheetsManager
from src.sheets.resume_extractor import ResumeExtractor
from src.ai.resume_analyzer import ResumeAnalyzer

def test_resume_processing():
    """Test the resume processing functionality"""
    try:
        sheets_manager = GoogleSheetsManager()
        resume_extractor = ResumeExtractor()
        
        print("Testing resume processing...")
        print(f"Sheet1 headers: {sheets_manager.get_sheet1_headers()}")
        print(f"Jobs headers: {sheets_manager.get_jobs_headers()}")
        
        # Test getting unscored resumes
        resumes = sheets_manager.get_unscored_resumes()
        print(f"Found {len(resumes)} resumes to process")
        
        if resumes:
            print("Sample resume data:")
            for i, resume in enumerate(resumes[:3]):
                print(f"Row {resume.row_index}: Position={resume.position}, URL={resume.resume_url}")
        
        # Test job matching
        if resumes:
            sample_resume = resumes[0]
            job_details = sheets_manager.get_job_details(sample_resume.position)
            if job_details:
                print(f"\nFound job details for '{sample_resume.position}':")
                print(f"Description: {job_details.description[:100]}...")
                print(f"Requirements: {job_details.requirements[:100]}...")
            else:
                print(f"\nNo job found for position: {sample_resume.position}")
        
        # Test resume extraction
        if resumes:
            sample_resume = resumes[0]
            content = resume_extractor.extract_content(sample_resume.resume_url)
            if content:
                print(f"\nExtracted resume content length: {len(content)} characters")
                # Show first 500 characters of actual text (skip PDF headers)
                clean_content = content.strip()
                if len(clean_content) > 500:
                    print(f"First 500 chars: {clean_content[:500]}...")
                else:
                    print(f"Full content: {clean_content}")
            else:
                print(f"\nCould not extract content from: {sample_resume.resume_url}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_resume_processing() 
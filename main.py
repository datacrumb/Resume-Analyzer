import time
from typing import Set
from src.sheets.google_sheets import GoogleSheetsManager
from src.sheets.resume_extractor import ResumeExtractor
from src.ai.resume_analyzer import ResumeAnalyzer
from src.utils.config import PROCESSING_DELAY
from src.utils.logger import setup_logger, log_processing_start, log_resume_processing, log_resume_scored, log_error

class ResumeProcessor:
    """Main orchestrator for resume processing"""
    
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.resume_extractor = ResumeExtractor()
        self.resume_analyzer = ResumeAnalyzer()
        self.logger = setup_logger()
        self.processed_resumes: Set[str] = set()
    
    def process_unscored_resumes(self):
        """Process all resumes without scores"""
        try:
            # Get unscored resumes
            resumes = self.sheets_manager.get_unscored_resumes()
            log_processing_start(self.logger, len(resumes))
            
            for resume in resumes:
                try:
                    # Check if already processed
                    resume_hash = resume.create_hash()
                    if resume_hash in self.processed_resumes:
                        self.logger.info(f"Row {resume.row_index}: Already processed, skipping")
                        continue
                    
                    log_resume_processing(self.logger, resume.row_index, resume.position)
                    
                    # Get job details
                    job_details = self.sheets_manager.get_job_details(resume.position)
                    if not job_details:
                        self.logger.warning(f"Row {resume.row_index}: No matching job found for position '{resume.position}'")
                        continue
                    
                    # Extract resume content
                    resume_content = self.resume_extractor.extract_content(resume.resume_url)
                    if not resume_content:
                        self.logger.warning(f"Row {resume.row_index}: Could not extract resume content")
                        continue
                    
                    # Analyze with AI
                    result = self.resume_analyzer.analyze_resume(
                        resume_content=resume_content,
                        job_description=job_details.description,
                        requirements=job_details.requirements,
                        resume_url=resume.resume_url
                    )
                    
                    # Update score and reasoning in sheet
                    if result.get('score'):  # Only process if we have a valid score
                        if self.sheets_manager.update_resume_result(resume.row_index, result):
                            # Mark as processed
                            self.processed_resumes.add(resume_hash)
                            log_resume_scored(self.logger, resume.row_index, result['score'])
                    else:
                        print(f"Skipping row {resume.row_index}: No valid score generated")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(PROCESSING_DELAY)
                    
                except Exception as e:
                    log_error(self.logger, f"Error processing row {resume.row_index}", e)
                    continue
                    
        except Exception as e:
            log_error(self.logger, "Error in resume processing", e)

def main():
    """Main entry point"""
    processor = ResumeProcessor()
    processor.process_unscored_resumes()

if __name__ == "__main__":
    main()

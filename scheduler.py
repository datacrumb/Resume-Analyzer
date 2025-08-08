import schedule
import time
from src.utils.config import SCHEDULER_FREQUENCY, SCHEDULER_INTERVAL
from src.utils.logger import setup_logger
from main import ResumeProcessor

def run_scheduler():
    """Run the scheduler to process resumes periodically"""
    processor = ResumeProcessor()
    logger = setup_logger()
    
    # Schedule to run based on config
    schedule.every(SCHEDULER_FREQUENCY).seconds.do(processor.process_unscored_resumes)
    
    # Also run once immediately
    processor.process_unscored_resumes()
    
    logger.info(f"Scheduler started. Processing resumes every {SCHEDULER_FREQUENCY} seconds...")
    
    while True:
        schedule.run_pending()
        time.sleep(SCHEDULER_INTERVAL)  # Check every minute

if __name__ == "__main__":
    run_scheduler() 
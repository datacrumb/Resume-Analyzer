import logging
from datetime import datetime

def setup_logger(name: str = "resume_analysis"):
    """Setup logger for the application"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

def log_processing_start(logger, count: int):
    """Log processing start"""
    logger.info(f"Starting resume processing... Found {count} resumes to process")

def log_resume_processing(logger, row_index: int, position: str):
    """Log resume processing"""
    logger.info(f"Processing row {row_index}: Position={position}")

def log_resume_scored(logger, row_index: int, score: int):
    """Log resume scoring"""
    logger.info(f"Row {row_index}: Scored {score}/100")

def log_error(logger, message: str, error: Exception = None):
    """Log error"""
    if error:
        logger.error(f"{message}: {error}")
    else:
        logger.error(message) 
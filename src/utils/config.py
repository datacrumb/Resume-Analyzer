import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google Sheets Configuration
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET1_ID = os.getenv('SHEET1_ID')
JOBS_SHEET_ID = os.getenv('JOBS_SHEET_ID')

# Processing Configuration
PROCESSING_DELAY = 1  # seconds between processing each resume
SCHEDULER_INTERVAL = 60  # seconds between scheduler checks
SCHEDULER_FREQUENCY = 3600  # seconds (1 hour) between processing runs

# Column names (adjust these based on your actual sheet structure)
SHEET1_POSITION_COL = 4  # Position column (5th column, 0-indexed)
SHEET1_RESUME_URL_COL = 7  # Resume URL column (8th column, 0-indexed)

# Updated column mapping based on your new headers
SHEET1_SCORE_COL = 'Score'
SHEET1_REASONING_COL = 'Reasoning'
SHEET1_TECHNICAL_SKILLS_COL = 'Technical Skills Match'
SHEET1_EXPERIENCE_RELEVANCE_COL = 'Experience Relevance'
SHEET1_SOFT_SKILLS_COL = 'Soft Skills & Cultural Fit'
SHEET1_EDUCATION_CERT_COL = 'Education & Certifications'
SHEET1_CAREER_PROGRESSION_COL = 'Career Progression'

JOBS_TITLE_COL = 'Title'
JOBS_DESCRIPTION_COL = 'Description'
JOBS_REQUIREMENTS_COL = 'Requirements'

# AI Configuration
AI_MODEL = "gpt-4o-mini-2024-07-18"
AI_MAX_TOKENS = 1500  # Increased for more detailed responses
AI_TEMPERATURE = 0.3 


MISTRAL_OCR_API_KEY = os.getenv('MISTRAL_OCR_API_KEY')
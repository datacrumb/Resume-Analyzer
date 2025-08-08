import gspread
from typing import List, Tuple, Optional
from ..utils.config import (
    SPREADSHEET_ID, SHEET1_ID, JOBS_SHEET_ID,
    SHEET1_POSITION_COL, SHEET1_RESUME_URL_COL, SHEET1_SCORE_COL,
    JOBS_TITLE_COL, JOBS_DESCRIPTION_COL, JOBS_REQUIREMENTS_COL
)
from ..models.resume import Resume, JobDetails

class GoogleSheetsManager:
    """Handles Google Sheets operations"""
    
    def __init__(self):
        self.client = gspread.service_account(filename="credentials.json")
        # Set longer timeout for Google Sheets operations
        self.client.timeout = 60  # 60 seconds timeout
        self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
        self.sheet1 = self.spreadsheet.get_worksheet_by_id(int(SHEET1_ID))
        self.jobs_sheet = self.spreadsheet.get_worksheet_by_id(int(JOBS_SHEET_ID))
    
    def get_sheet1_headers(self) -> List[str]:
        """Get headers from Sheet1"""
        all_values = self.sheet1.get_all_values()
        return all_values[0] if all_values else []
    
    def get_jobs_headers(self) -> List[str]:
        """Get headers from Jobs sheet"""
        all_values = self.jobs_sheet.get_all_values()
        return all_values[0] if all_values else []
    
    def get_unscored_resumes(self) -> List[Resume]:
        """Get resumes that don't have scores yet"""
        all_values = self.sheet1.get_all_values()
        if not all_values:
            return []
        
        headers = all_values[0]
        resumes = []
        
        for i, row in enumerate(all_values[1:], start=2):
            # Check if score column (2nd-to-last column) is empty
            if len(row) > 0:
                # Score is in 2nd-to-last column, Reasoning in last column
                score_col_index = len(headers) - 2  # 2nd-to-last column
                
                # Check if score column exists and is empty
                if len(row) <= score_col_index or not row[score_col_index].strip():
                    if len(row) > max(SHEET1_POSITION_COL, SHEET1_RESUME_URL_COL):
                        position = row[SHEET1_POSITION_COL] if len(row) > SHEET1_POSITION_COL else ""
                        resume_url = row[SHEET1_RESUME_URL_COL] if len(row) > SHEET1_RESUME_URL_COL else ""
                        
                        if position and resume_url:
                            resume = Resume(
                                row_index=i,
                                position=position,
                                resume_url=resume_url
                            )
                            resumes.append(resume)
        
        return resumes
    
    def get_job_details(self, title: str) -> Optional[JobDetails]:
        """Find job details by title"""
        all_values = self.jobs_sheet.get_all_values()
        if not all_values:
            return None
        
        headers = all_values[0]
        
        # Find column indices
        try:
            title_idx = headers.index(JOBS_TITLE_COL)
            desc_idx = headers.index(JOBS_DESCRIPTION_COL)
            req_idx = headers.index(JOBS_REQUIREMENTS_COL)
        except ValueError:
            print(f"Required columns '{JOBS_TITLE_COL}', '{JOBS_DESCRIPTION_COL}', or '{JOBS_REQUIREMENTS_COL}' not found in Jobs sheet")
            return None
        
        # Search for matching title
        for row in all_values[1:]:
            if len(row) > title_idx and row[title_idx].strip().lower() == title.strip().lower():
                description = row[desc_idx] if len(row) > desc_idx else ""
                requirements = row[req_idx] if len(row) > req_idx else ""
                return JobDetails.from_tuple(title, description, requirements)
        
        return None
    
    def update_resume_result(self, row_index: int, result: dict) -> bool:
        """Update the score and reasoning for a specific resume row"""
        try:
            # Get the current headers to determine column positions
            all_values = self.sheet1.get_all_values()
            if not all_values:
                return False
            
            headers = all_values[0]
            total_cols = len(headers)
            
            # Score goes in second-to-last column, reasoning in last column
            score_col = total_cols - 2  # Second-to-last column (0-indexed)
            reasoning_col = total_cols - 1  # Last column (0-indexed)
            
            # Extract score and reasoning from result
            score = result.get('score', '')
            reasoning = result.get('reasoning', 'No reasoning provided')
            
            # Only update if we have a valid score
            if score and score != "":
                # Update both cells (convert to 1-indexed for gspread)
                self.sheet1.update_cell(row_index, score_col + 1, score)
                self.sheet1.update_cell(row_index, reasoning_col + 1, reasoning)
                
                print(f"Updated row {row_index}: Score={score}, Reasoning={reasoning[:50]}...")
                return True
            else:
                print(f"Skipping row {row_index}: No valid score to update")
                return False
                
        except Exception as e:
            print(f"Error updating result for row {row_index}: {e}")
            return False 
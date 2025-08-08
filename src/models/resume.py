from dataclasses import dataclass
from typing import Optional

@dataclass
class Resume:
    """Data model for a resume"""
    row_index: int
    position: str
    resume_url: str
    resume_content: Optional[str] = None
    score: Optional[int] = None
    
    def create_hash(self) -> str:
        """Create unique hash for deduplication"""
        return f"{self.position.lower().strip()}_{self.resume_url.lower().strip()}"

@dataclass
class JobDetails:
    """Data model for job details"""
    title: str
    description: str
    requirements: str
    
    @classmethod
    def from_tuple(cls, title: str, description: str, requirements: str):
        """Create JobDetails from tuple"""
        return cls(title=title, description=description, requirements=requirements) 
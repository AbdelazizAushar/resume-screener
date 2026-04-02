from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    resume_text: Optional[str] = None   # because it can be empty if the user uploads a pdf instead
    job_description: str

from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    resume_text: Optional[str] = None   # because it can be empty if the user uploads a pdf instead
    job_description: str


class LLMFeedback(BaseModel):
    strengths: str
    weaknesses: str
    suggestions: list[str]


class AnalyzeResponse(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    similarity_score: float
    llm_feedback: Optional[LLMFeedback] = None
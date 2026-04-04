from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging

from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.keyword_extractor import compare_keywords
from backend.services.similarity_scorer import compute_similarity
from backend.services.llm_feedback import get_llm_feedback

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
):
    if not resume_text and not resume_file:
        raise HTTPException(
            status_code=400,
            detail="Please provide either resume text or a PDF file.",
        )

    if resume_file:
        file_bytes = await resume_file.read()
        try:
            resume_text = extract_text_from_pdf(file_bytes)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    keyword_results = compare_keywords(resume_text, job_description)
    similarity_score = compute_similarity(resume_text, job_description)

    feedback = None
    try:
        feedback = get_llm_feedback(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=keyword_results["matched_skills"],
            missing_skills=keyword_results["missing_skills"],
            similarity_score=similarity_score,
        )
    except Exception as e:
        logger.warning(f"LLM feedback failed: {e}")

    return {
        "matched_skills": keyword_results["matched_skills"],
        "missing_skills": keyword_results["missing_skills"],
        "similarity_score": similarity_score,
        "llm_feedback": feedback,
    }

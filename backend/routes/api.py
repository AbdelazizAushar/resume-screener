from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.keyword_extractor import compare_keywords
from backend.services.similarity_scorer import compute_similarity

router = APIRouter()


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

    return {
        "resume_text": resume_text,
        "job_description": job_description,
        "matched_skills": keyword_results["matched_skills"],
        "missing_skills": keyword_results["missing_skills"],
        "similarity_score": similarity_score,
    }

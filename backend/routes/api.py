from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from backend.services.pdf_parser import extract_text_from_pdf

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

    # extract text from pdf (if found)
    if resume_file:
        file_bytes = await resume_file.read()
        try:
            resume_text = extract_text_from_pdf(file_bytes)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    # will just return anything now
    return {
        "resume_text": resume_text,
        "job_description": job_description,
    }

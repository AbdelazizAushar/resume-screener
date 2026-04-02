from fastapi import FastAPI
from backend.routes.api import router

app = FastAPI(
    title="Resume Screener API",
    description="AI-powered resume analysis tool that matches resumes to job descriptions.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

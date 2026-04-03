import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token

_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(resume_text: str, job_description: str) -> float:
    if not resume_text.strip() or not job_description.strip():
        raise ValueError("Resume and job description must not be empty.")

    resume_embedding = _model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = _model.encode(job_description, convert_to_tensor=True)

    cosine_score = util.cos_sim(resume_embedding, jd_embedding)

    score = float(cosine_score[0][0])
    score = max(0.0, min(1.0, score))

    return round(score * 100, 2)

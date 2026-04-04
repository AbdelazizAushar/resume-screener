import os
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    provider="auto",
    api_key=os.getenv("HF_TOKEN"),
)


def get_llm_feedback(
    resume_text: str,
    job_description: str,
    matched_skills: list[str],
    missing_skills: list[str],
    similarity_score: float,
) -> dict:
    prompt = f"""You are an expert technical recruiter. Analyze this resume against the job description and return structured feedback.

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{job_description}

--- ANALYSIS RESULTS ---
Similarity Score: {similarity_score}/100
Matched Skills: {", ".join(matched_skills) if matched_skills else "None"}
Missing Skills: {", ".join(missing_skills) if missing_skills else "None"}

Respond ONLY with a valid JSON object. No markdown, no backticks, no explanation — just raw JSON.

{{
  "strengths": "A short paragraph on what the resume does well for this role.",
  "weaknesses": "A short paragraph on where the resume falls short.",
  "suggestions": [
    "Specific suggestion 1",
    "Specific suggestion 2",
    "Specific suggestion 3"
  ]
}}"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1
    raw = raw[start:end]

    return json.loads(raw)

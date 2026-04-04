import csv
import json
import re
from pathlib import Path

TAXONOMY_PATH = Path(__file__).parent.parent.parent / "skills_en.csv"
EXTRA_SKILLS_PATH = Path(__file__).parent.parent.parent / "extra_skills.json"

_SKILL_SET: set[str] = set()


def _load_taxonomy() -> set[str]:
    global _SKILL_SET
    if _SKILL_SET:
        return _SKILL_SET

    skills = set()

    if TAXONOMY_PATH.exists():
        with open(TAXONOMY_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                preferred = row.get("PREFERREDLABEL", "").strip().lower()
                if preferred:
                    skills.add(preferred)

                for alt in row.get("ALTLABELS", "").split("\n"):
                    alt = alt.strip().lower()
                    if alt:
                        skills.add(alt)

    if EXTRA_SKILLS_PATH.exists():
        with open(EXTRA_SKILLS_PATH, encoding="utf-8") as f:
            for skill in json.load(f):
                skills.add(skill.strip().lower())

    if not skills:
        raise FileNotFoundError(
            "No skill sources found. Please add skills_en.csv"
            " and/or extra_skills.json to the project directory."
        )

    _SKILL_SET = skills
    return _SKILL_SET


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\/\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _deduplicate(skills: set[str]) -> set[str]:
    sorted_skills = sorted(skills, key=len, reverse=True)
    result = []
    for skill in sorted_skills:
        if not any(skill in longer for longer in result):
            result.append(skill)
    return set(result)


def _scan_for_skills(text: str, taxonomy: set[str]) -> set[str]:
    normalized_text = _normalize(text)
    found = set()

    for skill in sorted(taxonomy, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(_normalize(skill)) + r"(?!\w)"
        if re.search(pattern, normalized_text):
            found.add(skill)

    return _deduplicate(found)


def extract_keywords(text: str) -> set[str]:
    return _scan_for_skills(text, _load_taxonomy())


def compare_keywords(resume_text: str, job_description: str) -> dict:
    taxonomy = _load_taxonomy()

    resume_skills = _scan_for_skills(resume_text, taxonomy)
    jd_skills = _scan_for_skills(job_description, taxonomy)

    return {
        "matched_skills": list(resume_skills & jd_skills),
        "missing_skills": list(jd_skills - resume_skills),
    }
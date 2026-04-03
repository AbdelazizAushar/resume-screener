import spacy

nlp = spacy.load("en_core_web_sm")


# maybe change later as this is not 100% good
def extract_keywords(text: str) -> set:
    doc = nlp(text.lower())
    keywords = set()

    for chunk in doc.noun_chunks:
        lemma = chunk.lemma_.strip()
        if len(lemma) > 2 and not all(token.is_stop for token in chunk):
            keywords.add(lemma)

    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and not token.is_stop and len(token.lemma_) > 2:
            keywords.add(token.lemma_.strip())

    return keywords


def compare_keywords(resume_text: str, job_description: str) -> dict:
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    matched = list(resume_keywords & jd_keywords)
    missing = list(jd_keywords - resume_keywords)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
    }

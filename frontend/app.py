import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Resume Screener",
    page_icon="📄",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Libre Baskerville', Georgia, serif;
    background-color: #f7f5f0;
    color: #111111;
}
.stApp { background-color: #f7f5f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1100px; }

/* ── Top bar ── */
.topbar {
    width: 100%;
    height: 5px;
    background-color: #111111;
    margin-bottom: 3rem;
}

/* ── Header ── */
.site-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid #111;
    padding-bottom: 1rem;
    margin-bottom: 3rem;
}
.site-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #111;
}
.site-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #888;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Field labels ── */
.field-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.5rem;
    display: block;
}

/* ── Textareas ── */
.stTextArea textarea {
    background-color: #ffffff !important;
    border: 1px solid #d0cdc8 !important;
    border-radius: 3px !important;
    color: #111 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    box-shadow: none !important;
}
.stTextArea textarea:focus {
    border-color: #111 !important;
    box-shadow: none !important;
    caret-color: #c0392b !important;
}
.stTextArea label { display: none !important; }

/* ── Radio ── */
.stRadio > div {
    flex-direction: row !important;
    gap: 1.5rem;
}
.stRadio div[role="radiogroup"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #111 !important;
    font-weight: 500 !important;
}
.stRadio div[role="radiogroup"] label p {
    color: #111 !important;
}
.stRadio > label { display: none !important; }

/* ── Radio selected indicator ── */
.stRadio div[role="radiogroup"] label div[data-testid="stWidgetLabel"] p { color: #111 !important; }
[data-baseweb="radio"] [data-checked="true"] div,
[data-baseweb="radio"] div:has(> input:checked) ~ div {
    background-color: #111 !important;
    border-color: #111 !important;
}
[data-baseweb="radio"] [data-checked="true"] svg { fill: #111 !important; }
[data-baseweb="radio"] svg { color: #111 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #fff;
    border: 1px solid #d0cdc8;
    border-radius: 3px;
    padding: 1rem;
}
[data-testid="stFileUploader"] label { display: none !important; }

/* ── Button ── */
.stButton > button {
    background-color: #111111 !important;
    color: #f7f5f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: background-color 0.15s ease !important;
}
.stButton > button:hover {
    background-color: #333 !important;
}
            
.stButton > button p,
.stButton > button span {
    color: #f7f5f0 !important;
}

/* ── Divider ── */
.rule {
    border: none;
    border-top: 1px solid #d0cdc8;
    margin: 2.5rem 0;
}
.rule-heavy {
    border: none;
    border-top: 2px solid #111;
    margin: 2.5rem 0;
}

/* ── Score block ── */
.score-wrap {
    padding: 2rem 0 1.5rem 0;
}
.score-figure {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 7rem;
    font-weight: 600;
    line-height: 1;
    color: #111;
    letter-spacing: -0.04em;
}
.score-denom {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem;
    color: #bbb;
    font-weight: 400;
}
.score-descriptor {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #888;
    margin-top: 0.4rem;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background-color: #e5e2dc !important;
    border-radius: 0 !important;
    height: 3px !important;
}
.stProgress > div > div > div {
    background-color: #111 !important;
    border-radius: 0 !important;
}

/* ── Skills ── */
.skills-section { margin: 2rem 0; }
.skills-group-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.8rem;
}
.skills-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.skill-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    padding: 0.25rem 0.7rem;
    border-radius: 2px;
    letter-spacing: 0.02em;
}
.skill-tag-matched {
    background-color: #111;
    color: #f7f5f0;
}
.skill-tag-missing {
    background-color: transparent;
    color: #c0392b;
    border: 1px solid #c0392b;
}

/* ── Feedback ── */
.feedback-block {
    margin: 2rem 0;
}
.feedback-heading {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.6rem;
}
.feedback-body {
    font-family: 'Libre Baskerville', serif;
    font-size: 0.9rem;
    line-height: 1.8;
    color: #333;
}
.suggestion-row {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 0.9rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid #e5e2dc;
}
.suggestion-row:last-child { border-bottom: none; }
.suggestion-index {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #bbb;
    padding-top: 0.2rem;
    flex-shrink: 0;
    width: 1.2rem;
}
.suggestion-text {
    font-family: 'Libre Baskerville', serif;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #333;
}

/* ── Status widget ── */
[data-testid="stStatusWidget"] p,
[data-testid="stStatusWidget"] span,
[data-testid="stStatusWidget"] div,
[data-testid="stStatus"] p,
[data-testid="stStatus"] span,
[data-testid="stMarkdownContainer"] p { color: #111111 !important; }

/* ── Inline error messages ── */
.inline-error {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #c0392b;
    border: 1px solid #c0392b;
    border-radius: 3px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0;
    background-color: #fff5f5;
}
</style>
""", unsafe_allow_html=True)

# ── Top bar + header ────────────────────────────────────────────────────────────
st.markdown('<div class="topbar"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="site-header">
    <div class="site-title">Resume Screener</div>
    <div class="site-meta">AI-powered · Job match analysis</div>
</div>
""", unsafe_allow_html=True)

# ── Inputs ──────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<span class="field-label">Job Description</span>',
                unsafe_allow_html=True)
    job_description = st.text_area(
        label="jd",
        placeholder="Paste the job description here…",
        height=300,
        label_visibility="collapsed",
    )

with col2:
    st.markdown('<span class="field-label">Resume</span>',
                unsafe_allow_html=True)

    input_method = st.radio(
        "input_method",
        ["Paste text", "Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
    )

    resume_text = ""
    resume_file = None

    if input_method == "Paste text":
        resume_text = st.text_area(
            label="resume",
            placeholder="Paste your resume here…",
            height=255,
            label_visibility="collapsed",
        )
    else:
        resume_file = st.file_uploader(
            "resume_pdf",
            type=["pdf"],
            label_visibility="collapsed",
        )

st.markdown("<br>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    analyze = st.button("Analyze →")

# ── Analysis ────────────────────────────────────────────────────────────────────


def show_error(msg):
    st.markdown(
        f'<div class="inline-error">{msg}</div>', unsafe_allow_html=True)


if analyze:
    if not job_description.strip():
        show_error("Please enter a job description.")
        st.stop()
    if input_method == "Paste text" and not resume_text.strip():
        show_error("Please paste your resume text.")
        st.stop()
    if input_method == "Upload PDF" and resume_file is None:
        show_error("Please upload a PDF resume.")
        st.stop()

    status = st.status("Running analysis…", expanded=True)
    try:
        with status:
            data = {"job_description": job_description}
            files = {}

            if input_method == "Paste text":
                data["resume_text"] = resume_text
            else:
                files["resume_file"] = (
                    resume_file.name, resume_file.getvalue(), "application/pdf"
                )

            st.markdown(
                '<p style="color:#111111;font-family:IBM Plex Mono,monospace;font-size:0.78rem;margin:0.3rem 0;">Extracting keywords…</p>', unsafe_allow_html=True)
            st.markdown('<p style="color:#111111;font-family:IBM Plex Mono,monospace;font-size:0.78rem;margin:0.3rem 0;">Computing semantic similarity…</p>', unsafe_allow_html=True)
            st.markdown(
                '<p style="color:#111111;font-family:IBM Plex Mono,monospace;font-size:0.78rem;margin:0.3rem 0;">Generating LLM feedback…</p>', unsafe_allow_html=True)

            response = requests.post(
                f"{API_URL}/analyze",
                data=data,
                files=files if files else None,
            )
            response.raise_for_status()
            result = response.json()

        status.update(label="Analysis complete.",
                      state="complete", expanded=False)

    except requests.exceptions.ConnectionError:
        status.update(label="Connection failed.",
                      state="error", expanded=False)
        show_error("Cannot connect to the backend at http://localhost:8000")
        st.stop()
    except requests.exceptions.HTTPError as e:
        status.update(label="Request failed.", state="error", expanded=False)
        show_error(f"API error: {e.response.text}")
        st.stop()
    except Exception as e:
        status.update(label="Something went wrong.",
                      state="error", expanded=False)
        show_error(f"{e}")
        st.stop()

    # ── Results ─────────────────────────────────────────────────────────────────
    score = result.get("similarity_score", 0)
    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])
    feedback = result.get("llm_feedback", {})

    st.markdown('<hr class="rule-heavy">', unsafe_allow_html=True)

    # Score
    score_int = int(round(score))
    st.markdown(f"""
    <div class="score-wrap">
        <div class="score-figure">{score_int}<span class="score-denom">/100</span></div>
        <div class="score-descriptor">Semantic match score</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(score_int / 100)

    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    # Skills
    sk1, sk2 = st.columns(2, gap="large")

    with sk1:
        matched_tags = "".join(
            f'<span class="skill-tag skill-tag-matched">{s}</span>' for s in matched
        ) if matched else '<span style="font-family:IBM Plex Mono,monospace;font-size:0.75rem;color:#bbb;">—</span>'
        st.markdown(f"""
        <div class="skills-section">
            <div class="skills-group-label">Matched skills</div>
            <div class="skills-list">{matched_tags}</div>
        </div>
        """, unsafe_allow_html=True)

    with sk2:
        missing_tags = "".join(
            f'<span class="skill-tag skill-tag-missing">{s}</span>' for s in missing
        ) if missing else '<span style="font-family:IBM Plex Mono,monospace;font-size:0.75rem;color:#bbb;">None — full coverage</span>'
        st.markdown(f"""
        <div class="skills-section">
            <div class="skills-group-label">Missing skills</div>
            <div class="skills-list">{missing_tags}</div>
        </div>
        """, unsafe_allow_html=True)

    if feedback:
        st.markdown('<hr class="rule">', unsafe_allow_html=True)

        fb1, fb2 = st.columns(2, gap="large")

        with fb1:
            if feedback.get("strengths"):
                st.markdown(f"""
                <div class="feedback-block">
                    <div class="feedback-heading">Strengths</div>
                    <div class="feedback-body">{feedback["strengths"]}</div>
                </div>
                """, unsafe_allow_html=True)

        with fb2:
            if feedback.get("weaknesses"):
                st.markdown(f"""
                <div class="feedback-block">
                    <div class="feedback-heading">Weaknesses</div>
                    <div class="feedback-body">{feedback["weaknesses"]}</div>
                </div>
                """, unsafe_allow_html=True)

        if feedback.get("suggestions"):
            st.markdown('<hr class="rule">', unsafe_allow_html=True)
            st.markdown(
                '<div class="feedback-heading">Suggestions</div>', unsafe_allow_html=True)

            rows = "".join(
                f"""<div class="suggestion-row">
                    <div class="suggestion-index">0{i+1}</div>
                    <div class="suggestion-text">{s}</div>
                </div>"""
                for i, s in enumerate(feedback["suggestions"])
            )
            st.markdown(rows, unsafe_allow_html=True)

    # ── Toast + auto-scroll ─────────────────────────────────────────────────
    st.toast("Analysis ready — results below.", icon=None)
    st.markdown("""
    <script>
        window.setTimeout(function() {
            const results = window.parent.document.querySelector('[data-testid="stHorizontalBlock"]');
            if (results) {
                results.scrollIntoView({ behavior: "smooth", block: "start" });
            } else {
                window.parent.scrollTo({ top: window.parent.document.body.scrollHeight, behavior: "smooth" });
            }
        }, 300);
    </script>
    """, unsafe_allow_html=True)

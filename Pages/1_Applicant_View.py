import io
import re
import streamlit as st
from PyPDF2 import PdfReader
import docx2txt
from sentence_transformers import SentenceTransformer, util
from fpdf import FPDF

# ============================================================
# ✅ Load model safely (cached)
# ============================================================
@st.cache_resource
def load_model():
    try:
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return SentenceTransformer("paraphrase-MiniLM-L6-v2")

model = load_model()

# ============================================================
# ✅ Extract text functions
# ============================================================
def extract_text_from_pdf(uploaded_file):
    try:
        pdf = PdfReader(uploaded_file)
        return " ".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        return f"[Error reading PDF: {e}]"

def extract_text_from_docx(uploaded_file):
    try:
        return docx2txt.process(uploaded_file)
    except Exception as e:
        return f"[Error reading DOCX: {e}]"

def get_text(file):
    if not file:
        return ""
    name = file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file)
    elif name.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")
    return ""

# ============================================================
# ✅ Job title extractor
# ============================================================
def extract_job_title(jd_text: str) -> str:
    if not jd_text or not isinstance(jd_text, str):
        return "the advertised position"

    patterns = [
        r"(?:title|position|role)\s*[:\-]\s*([A-Za-z0-9\s/&]+)",
        r"\b(?:for|as)\s+a[n]?\s+([A-Z][A-Za-z\s/&]+)",
        r"([A-Z][A-Za-z\s/&]+)\s*(?:position|role|opportunity)",
    ]

    for pat in patterns:
        match = re.search(pat, jd_text, re.IGNORECASE)
        if match:
            title = re.sub(r"[^A-Za-z0-9\s/&-]", "", match.group(1).strip())
            return title[:60]

    for line in jd_text.split("\n"):
        if any(w in line.lower() for w in ["engineer", "analyst", "scientist", "developer", "manager", "intern", "specialist"]):
            return line.strip().split(":")[0]

    return "the advertised position"

# ============================================================
# ✅ ATS Score Calculator
# ============================================================
def calculate_ats_score(resume_text, jd_text):
    if not resume_text or not jd_text:
        return 0.0
    emb = model.encode([resume_text, jd_text], convert_to_tensor=True)
    sim = util.cos_sim(emb[0], emb[1])
    return round(float(sim.item()) * 100, 2)

# ============================================================
# ✅ Cover Letter Generator
# ============================================================
def generate_cover_letter(resume_text: str, jd_text: str):
    """Generate a clean and human-like cover letter."""
    if not resume_text or not jd_text:
        return "Please provide both resume and job description text.", None

    def clean_text(t):
        t = re.sub(r"[^a-zA-Z0-9\s]", " ", t.lower())
        return re.sub(r"\s+", " ", t).strip()

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_tokens = list(set(resume_clean.split()))
    jd_tokens = list(set(jd_clean.split()))

    if not resume_tokens or not jd_tokens:
        return "Insufficient text to analyze.", None

    resume_emb = model.encode(resume_tokens, convert_to_tensor=True)
    jd_emb = model.encode(jd_tokens, convert_to_tensor=True)
    sim_matrix = util.cos_sim(resume_emb, jd_emb)

    matched = []
    threshold = 0.65
    for i, r_word in enumerate(resume_tokens):
        for j, j_word in enumerate(jd_tokens):
            if sim_matrix[i][j] > threshold:
                matched.append(j_word)

    matched_text = ", ".join(sorted(set(matched[:12]))) or "key analytical and technical skills"
    missing_text = ", ".join(sorted(set(jd_tokens[:8]) - set(matched))) or "emerging technologies and methodologies"

    job_title = extract_job_title(jd_text)

    text = (
        f"Dear Hiring Manager,\n\n"
        f"I am excited to apply for {job_title}. My experience and skills align closely with the requirements outlined in the job description.\n\n"
        f"I bring proven strengths in {matched_text}, which I have applied to deliver measurable results and drive process improvements. "
        f"I am eager to continue developing expertise in {missing_text} to contribute meaningfully to your organization's goals.\n\n"
        f"I am confident that my problem-solving mindset, adaptability, and technical foundation make me a strong fit for this role.\n\n"
        f"Thank you for considering my application. I look forward to the opportunity to discuss how I can add value to your team.\n\n"
        f"Sincerely,\nAnitha Morampudi"
    )

    # --- PDF generation ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    safe_text = re.sub(r"[^\x00-\x7F]+", " ", text)
    safe_text = re.sub(r"(\S{60,})", lambda m: m.group(1)[:60] + " ", safe_text)

    for line in safe_text.split("\n"):
        try:
            pdf.multi_cell(w=190, h=8, txt=line.strip(), align="L")
        except Exception:
            pdf.multi_cell(w=190, h=8, txt=line.strip()[:180], align="L")

    pdf_bytes = pdf.output(dest="S").encode("latin-1", "replace")
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return text, pdf_buffer

# ============================================================
# ✅ Streamlit App Layout
# ============================================================
st.title("🧑‍💼 Applicant View - ATS Score & Cover Letter Generator")

st.subheader("📄 Upload Your Resume")
resume_upload = st.file_uploader("Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
resume_text_manual = st.text_area("Or Paste Resume Text", height=150)

st.subheader("💼 Upload or Paste Job Description")
jd_upload = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
jd_text_manual = st.text_area("Or Paste Job Description", height=150)

if st.button("🚀 Analyze & Generate"):
    resume_text = resume_text_manual or get_text(resume_upload)
    jd_text = jd_text_manual or get_text(jd_upload)

    if not resume_text or not jd_text:
        st.warning("⚠️ Please provide both resume and job description.")
    else:
        ats_score = calculate_ats_score(resume_text, jd_text)
        st.metric("🎯 ATS Match Score", f"{ats_score}%")

        resume_words = set(re.findall(r"\b\w+\b", resume_text.lower()))
        jd_words = set(re.findall(r"\b\w+\b", jd_text.lower()))
        matched = sorted(list(resume_words & jd_words))
        missing = sorted(list(jd_words - resume_words))[:50]

        st.success(f"✅ Matched Keywords ({len(matched)}):")
        st.write(", ".join(matched[:50]))
        st.error(f"❌ Missing Keywords ({len(missing)}):")
        st.write(", ".join(missing))

        text, pdf_buffer = generate_cover_letter(resume_text, jd_text)
        st.subheader("✉️ Generated Cover Letter")
        st.text_area("Preview", text, height=350)
        st.download_button(
            label="⬇️ Download Cover Letter PDF",
            data=pdf_buffer,
            file_name="cover_letter.pdf",
            mime="application/pdf",
        )

import re
import io
import torch
from fpdf import FPDF
from sentence_transformers import SentenceTransformer, util

# Load once globally
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------------------
# Utility: Extract Contact Info
# -----------------------------------------------
def extract_contact_info(resume_text: str):
    """Extracts name, email, and phone robustly (handles ALL CAPS)."""
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
    phone = re.search(r"(\+?\d[\d\s().-]{7,}\d)", resume_text)

    # Split into clean lines
    lines = [l.strip() for l in resume_text.split("\n") if l.strip()]

    name = None
    for line in lines[:8]:  # look at first few lines
        # Match Firstname Lastname even in all caps
        if re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+$", line) or re.match(r"^[A-Z]+\s+[A-Z]+$", line):
            name = line.strip().title()
            break

    return (
        name if name else None,
        email.group(0) if email else "",
        phone.group(0) if phone else "",
    )

# -----------------------------------------------
# Utility: Extract Job Title
# -----------------------------------------------
def extract_job_title(jd_text: str):
    """Extract probable job title."""
    if not jd_text:
        return "the advertised position"

    for line in jd_text.split("\n"):
        if re.search(r"\b(data|ai|ml|software|business|product|analyst|engineer|developer|scientist|manager|intern)\b", line.lower()):
            clean = re.sub(r"[^A-Za-z\s/&-]", "", line).strip()
            return " ".join(clean.split()[:5]).title()
    return "the advertised position"

# -----------------------------------------------
# Cover Letter Generator
# -----------------------------------------------
def generate_cover_letter(resume_text: str, jd_text: str):
    """Generate polished, role-agnostic, skill-filtered cover letter."""
    if not resume_text or not jd_text:
        return "Please provide both resume and job description text.", None

    # --- Text Cleaning ---
    def clean_text(t):
        t = re.sub(r"[^a-zA-Z0-9\s]", " ", t.lower())
        return re.sub(r"\s+", " ", t).strip()

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_tokens = [t for t in resume_clean.split() if len(t) > 2]
    jd_tokens = [t for t in jd_clean.split() if len(t) > 2]

    # --- Stopwords & Verb Filtering ---
    stopwords = set("""
    is are was were be been being have has had do does did done can will would should could may might must
    a an the in of on for to from by with this that these those and or as at about into it its your you
    use using used developed implemented created designed delivered managed analyzed improved applied worked
    """.split())

    resume_emb = model.encode(resume_tokens, convert_to_tensor=True)
    jd_emb = model.encode(jd_tokens, convert_to_tensor=True)
    sim_matrix = util.cos_sim(resume_emb, jd_emb)

    matched, missing = set(), set()
    for i, r_word in enumerate(resume_tokens):
        if r_word in stopwords:
            continue
        max_score = torch.max(sim_matrix[i]).item()
        if max_score > 0.7:
            matched.add(r_word)
        elif 0.5 < max_score <= 0.7:
            missing.add(r_word)

    def is_skill(word):
        return not re.match(r".*(ing|ed|es|ly|able|ive|ment|ness|tion)$", word)

    matched = [w for w in matched if is_skill(w)]
    missing = [w for w in missing if is_skill(w)]

    matched_text = ", ".join(sorted(list(matched)[:10])) or "data analysis, visualization, and reporting"
    missing_text = ", ".join(sorted(list(missing)[:6])) or "emerging technologies and automation"

    # --- Info Extraction ---
    name, email, phone = extract_contact_info(resume_text)
    job_title = extract_job_title(jd_text)

    # --- Letter Body ---
    text = f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} role. My experience and skill set align well with the qualifications described in the posting.

Throughout my professional journey, I have developed strengths in {matched_text}, which have enabled me to drive measurable results, streamline workflows, and deliver data-driven outcomes. I am also eager to broaden my expertise in {missing_text}, continually adapting to new technologies and business needs.

I take pride in my analytical thinking, adaptability, and commitment to excellence. I am confident that my technical foundation and collaborative mindset would make me a valuable addition to your team.

Thank you for your time and consideration. I look forward to the opportunity to discuss how my background can add value to your organization.
"""

    # --- Smart signature ---
    if name:
        text += f"\nSincerely,\n{name}"
    else:
        text += "\nSincerely,\n"

    contact_line = " | ".join(filter(None, [email, phone]))
    if contact_line:
        text += f"\n{contact_line}"

    # --- PDF Output ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    safe_text = re.sub(r"[^\x00-\x7F]+", " ", text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(w=190, h=8, txt=line.strip(), align="L")

    pdf_bytes = bytes(pdf.output(dest="S"))
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return text, pdf_buffer

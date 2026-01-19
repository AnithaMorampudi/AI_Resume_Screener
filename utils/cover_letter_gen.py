import re
import io
import torch
from fpdf import FPDF
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_contact_info(resume_text: str):
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
    phone = re.search(r"(\+?\d[\d\s().-]{7,}\d)", resume_text)

    lines = [l.strip() for l in resume_text.split("\n") if l.strip()]
    name = None
    for line in lines[:8]:
        if re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+$", line) or re.match(r"^[A-Z]+\s+[A-Z]+$", line):
            name = line.title()
            break

    return name, email.group(0) if email else "", phone.group(0) if phone else ""


def extract_job_title(jd_text: str):
    if not jd_text:
        return "the advertised position"

    for line in jd_text.split("\n"):
        if re.search(
            r"\b(data|ai|ml|software|business|product|analyst|engineer|developer|scientist|manager|intern)\b",
            line.lower(),
        ):
            clean = re.sub(r"[^A-Za-z\s/&-]", "", line)
            return " ".join(clean.split()[:5]).title()

    return "the advertised position"


def generate_cover_letter(resume_text: str, jd_text: str):
    if not resume_text or not jd_text:
        return "Please provide both resume and job description text.", None

    def clean_text(t):
        t = re.sub(r"[^a-zA-Z0-9\s]", " ", t.lower())
        return re.sub(r"\s+", " ", t).strip()

    resume_tokens = clean_text(resume_text).split()
    jd_tokens = clean_text(jd_text).split()

    resume_emb = model.encode(resume_tokens, convert_to_tensor=True)
    jd_emb = model.encode(jd_tokens, convert_to_tensor=True)
    sim_matrix = util.cos_sim(resume_emb, jd_emb)

    matched = set()
    for i, word in enumerate(resume_tokens):
        if torch.max(sim_matrix[i]).item() > 0.7:
            matched.add(word)

    matched_text = ", ".join(sorted(list(matched)[:10])) or "data analysis and reporting"

    name, email, phone = extract_contact_info(resume_text)
    job_title = extract_job_title(jd_text)

    text = f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} role. With a strong passion for using data, analytics, and technology to drive meaningful insights, I am excited about the opportunity to contribute to your team and support data-driven decision-making.

I bring hands-on experience in {matched_text}, which I have applied across academic projects and practical problem-solving scenarios. My work has involved analyzing structured and unstructured data, building logical workflows, and transforming raw information into clear, actionable insights that support business and operational goals.

In addition to my technical capabilities, I offer strong analytical thinking, problem-solving skills, and attention to detail. I am comfortable working independently as well as collaborating with cross-functional teams, and I take pride in communicating complex ideas in a clear and concise manner to both technical and non-technical stakeholders.

I am continuously motivated to expand my skill set and stay current with evolving tools and methodologies. I actively seek opportunities to improve efficiency, automate repetitive processes, and deliver high-quality results under deadlines. I value feedback, adaptability, and accountability, and I approach every task with a strong sense of ownership.

What particularly draws me to this opportunity is the chance to contribute in a role like {job_title}, where analytical rigor, curiosity, and impact are highly valued. I am confident that my technical foundation, strong work ethic, and eagerness to learn would allow me to make meaningful contributions to your organization.

Thank you for your time and consideration. I would welcome the opportunity to discuss how my background, skills, and interests align with your team’s goals and how I can contribute to your continued success.
"""


    if name:
        text += f"\nSincerely,\n{name}"

    if email or phone:
        text += f"\n{email} {phone}"

    # ---- PDF generation ----
    def sanitize_text(t):
        t = re.sub(r"[^\x00-\x7F]+", " ", t)
        t = re.sub(r"(\S{60,})", lambda m: m.group(1)[:60] + " ", t)
        return t

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=11)

    safe_text = sanitize_text(text)
    for line in safe_text.split("\n"):
        pdf.multi_cell(180, 7, line)

    pdf_bytes = bytes(pdf.output(dest="S"))
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return text, pdf_buffer

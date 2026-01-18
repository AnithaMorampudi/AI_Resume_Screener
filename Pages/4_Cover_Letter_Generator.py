import streamlit as st
from utils.text_extraction import get_text
from utils.cover_letter_gen import generate_cover_letter

st.title("✉️ AI Cover Letter Generator")
st.write("Upload or paste your resume and job description to generate a tailored cover letter.")

st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
resume_text_manual = st.text_area("Or Paste Resume Text Here", height=150)

st.subheader("💼 Upload or Paste Job Description")
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
jd_text_manual = st.text_area("Or Paste Job Description Text Here", height=150)

if st.button("✨ Generate Cover Letter"):
    resume_text = resume_text_manual or get_text(resume_file)
    jd_text = jd_text_manual or get_text(jd_file)

    if not resume_text or not jd_text:
        st.warning("⚠️ Please provide both files.")
    else:
        text, pdf_buffer = generate_cover_letter(resume_text, jd_text)
        st.success("✅ Cover Letter Generated Successfully!")
        st.text_area("📜 Preview", text, height=350)
        st.download_button("⬇️ Download Cover Letter PDF", pdf_buffer, "cover_letter.pdf", "application/pdf")

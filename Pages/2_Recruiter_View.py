import streamlit as st
from utils.text_extraction import extract_text_from_pdf
from utils.resume_matcher import analyze_resume
import pandas as pd

st.title("🏢 Recruiter View")
st.write("Upload multiple resumes and one job description to rank best-fit candidates.")

resumes = st.file_uploader("📂 Upload Resumes", type=["pdf"], accept_multiple_files=True)
job_description = st.text_area("💼 Paste Job Description", height=200)

if st.button("📊 Match Resumes"):
    if not resumes or not job_description.strip():
        st.warning("⚠️ Upload resumes + paste job description.")
    else:
        st.info("Processing resumes …")
        data = []
        for file in resumes:
            text = extract_text_from_pdf(file)
            score = analyze_resume(text, job_description)
            data.append({"Resume": file.name, "Match Score (%)": score})
        df = pd.DataFrame(data).sort_values("Match Score (%)", ascending=False)
        st.success("✅ Matching Complete!")
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "⬇️ Download Results (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "resume_match_results.csv",
            "text/csv"
        )

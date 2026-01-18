import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""   # ensures CPU mode only
from sentence_transformers import SentenceTransformer, util
import re

# ------------------------------------------------------------
# Page Title and Info
# ------------------------------------------------------------
st.title("📊 Analytics Dashboard")
st.write("""
Compare your **Resume** and **Job Description** to uncover keyword overlap, missing skills, and text similarity.
""")

# ------------------------------------------------------------
# Inputs
# ------------------------------------------------------------
resume_text = st.text_area("📄 Paste your Resume Text", height=200)
jd_text = st.text_area("💼 Paste the Job Description", height=200)

if st.button("🔍 Analyze Texts"):
    if resume_text.strip() and jd_text.strip():
        st.info("Processing text and generating analytics...")

        # ------------------------------------------------------------
        # ✅ Clean and Tokenize Texts
        # ------------------------------------------------------------
        def clean_text(t):
            t = t.lower()
            t = re.sub(r'[^a-z0-9\s]', '', t)
            return t.split()

        resume_words = clean_text(resume_text)
        jd_words = clean_text(jd_text)

        # ------------------------------------------------------------
        # ✅ Keyword Overlap and Missing Words
        # ------------------------------------------------------------
        resume_counter = Counter(resume_words)
        jd_counter = Counter(jd_words)

        resume_set = set(resume_counter.keys())
        jd_set = set(jd_counter.keys())

        overlap = resume_set & jd_set
        missing = jd_set - resume_set

        overlap_pct = round(len(overlap) / len(jd_set) * 100, 2)

        # ------------------------------------------------------------
        # ✅ Similarity using SentenceTransformer
        # ------------------------------------------------------------
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
        sim_score = round(float(util.cos_sim(embeddings[0], embeddings[1])) * 100, 2)

        # ------------------------------------------------------------
        # ✅ Display Stats
        # ------------------------------------------------------------
        st.success(f"🧠 Text Similarity Score: **{sim_score}%**")
        st.info(f"🔁 Keyword Overlap: **{overlap_pct}%**")

        # ------------------------------------------------------------
        # ✅ Display Top Missing Keywords
        # ------------------------------------------------------------
        if missing:
            st.subheader("❌ Missing Keywords from Resume")
            st.write(", ".join(list(missing)[:20]))

        # ------------------------------------------------------------
        # ✅ Word Cloud Visualization
        # ------------------------------------------------------------
        st.subheader("☁️ Resume Word Cloud")
        resume_wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(resume_words))
        plt.imshow(resume_wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        st.subheader("☁️ Job Description Word Cloud")
        jd_wc = WordCloud(width=800, height=400, background_color="lightgrey").generate(" ".join(jd_words))
        plt.imshow(jd_wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        # ------------------------------------------------------------
        # ✅ Frequency Chart
        # ------------------------------------------------------------
        st.subheader("📈 Top 20 Resume Keywords (Frequency)")
        freq_df = pd.DataFrame(resume_counter.most_common(20), columns=["Keyword", "Count"])
        st.bar_chart(freq_df.set_index("Keyword"))

    else:
        st.warning("⚠️ Please paste both your Resume and Job Description text to proceed.")

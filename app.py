import streamlit as st

st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AI Resume Screener")
st.subheader("Navigate the application")

st.markdown(
    """
    This application contains multiple modules designed for different users.
    Select a section below to continue:
    """
)

col1, col2 = st.columns(2)

with col1:
    if st.button("👤 Applicant View"):
        st.switch_page("Pages/1_Applicant_View.py")

    if st.button("🧑‍💼 Recruiter View"):
        st.switch_page("Pages/2_Recruiter_View.py")

with col2:
    if st.button("📊 Analytics Dashboard"):
        st.switch_page("Pages/3_Analytics_Dashboard.py")

    if st.button("✉️ Cover Letter Generator"):
        st.switch_page("Pages/4_Cover_Letter_Generator.py")

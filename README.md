\# 🧠 AI Resume Screener \& Cover Letter Generator  



This project brings together AI, data science, and automation to make job applications smarter.  

It helps candidates instantly check how well their resume matches a job description and then auto-generates a personalized cover letter — all in one place.  



I built it using \*\*Streamlit\*\*, \*\*Python\*\*, and \*\*NLP (Sentence Transformers)\*\* to analyze the meaning of text rather than just keywords.  

The app shows your \*\*ATS (Applicant Tracking System) match score\*\*, highlights \*\*missing skills\*\*, and writes a clean, professional cover letter that fits the job posting.  



---



\## 🎥 Live Demo  



👉 \*\*Try the app here:\*\* \[https://ai-resume-screener-anithamorampudi.streamlit.app](https://ai-resume-screener-anithamorampudi.streamlit.app)  



\*(The link opens the live Streamlit app — upload your resume and a job description to see it in action!)\*  



---



\## 🚀 What the App Does  



\- \*\*ATS Score Check:\*\*  

&nbsp; Compares your resume and job description using semantic similarity to calculate a match percentage.  



\- \*\*Keyword Insights:\*\*  

&nbsp; Shows which important words, skills, or tools are missing from your resume.  



\- \*\*AI-Generated Cover Letter:\*\*  

&nbsp; Creates a tailored, human-sounding cover letter you can download as a PDF.  



\- \*\*Simple, No-Code UI:\*\*  

&nbsp; Just upload your resume and job description — everything else runs automatically.  



---



\## 🧠 How It Works  



1\. Upload your \*\*resume\*\* (PDF, DOCX, or TXT).  

2\. Paste or upload the \*\*job description\*\*.  

3\. The app uses the \*\*SentenceTransformer (all-MiniLM-L6-v2)\*\* model to compare text embeddings.  

4\. It returns:  

&nbsp;  - ✅ \*\*ATS match score\*\*  

&nbsp;  - 🧩 \*\*Matched \& missing keywords\*\*  

&nbsp;  - ✉️ \*\*Custom cover letter (PDF)\*\*  



---



\## 🛠️ Tech Stack  



| Category | Tools / Libraries |

|-----------|------------------|

| \*\*Framework\*\* | Streamlit |

| \*\*Language\*\* | Python |

| \*\*NLP Model\*\* | SentenceTransformer (`all-MiniLM-L6-v2`) |

| \*\*File Handling\*\* | PyPDF2, docx2txt |

| \*\*PDF Generation\*\* | fpdf2 |

| \*\*Environment\*\* | Anaconda (Python 3.12) |



---



\## ⚙️ Setup \& Run Locally  



```bash

\# Clone this repository

git clone https://github.com/AnithaMorampudi/AI-Resume-Screener.git

cd AI-Resume-Screener



\# (Optional) Create a virtual environment

conda create -n resume\_screener python=3.12

conda activate resume\_screener



\# Install dependencies

pip install -r requirements.txt



\# Run the Streamlit app

streamlit run app.py




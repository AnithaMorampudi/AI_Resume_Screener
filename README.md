# AI Resume Screener

## Overview
AI Resume Screener is an end-to-end AI-powered application designed to help job seekers and recruiters understand how well a resume matches a job description. Instead of relying only on exact keyword matching, the system uses Natural Language Processing (NLP) to capture semantic similarity, calculate an ATS-style match score, highlight skill gaps, and generate a tailored cover letter.

The goal of this project is to make resume screening more transparent, actionable, and efficient.

---

## What the Application Does
- Accepts resumes and job descriptions in PDF, DOCX, or TXT formats  
- Extracts and cleans unstructured text automatically  
- Calculates an ATS-style match score using semantic similarity  
- Identifies matched and missing keywords  
- Generates a role-aware, professional cover letter  
- Allows users to download the cover letter as a PDF  
- Provides a simple and interactive web interface built with Streamlit  

---

## Methods and Technical Approach

### Text Extraction
The application supports multiple document formats:
- **PDF** files are parsed using `PyPDF2`
- **DOCX** files are processed using `docx2txt`
- **TXT** files are read directly  

All documents are converted into plain text for analysis.

---

### Text Cleaning and Preprocessing
Extracted text is normalized by:
- Converting text to lowercase
- Removing special characters and unnecessary symbols
- Normalizing whitespace
- Tokenizing text into meaningful words  

This reduces noise while preserving important semantic information.

---

### Semantic Similarity Using NLP Embeddings
Instead of basic keyword matching, the system uses a pre-trained **Sentence Transformer model (`all-MiniLM-L6-v2`)** to generate semantic embeddings for both resumes and job descriptions.

These embeddings capture contextual meaning, allowing the system to recognize related skills even when different wording is used. Cosine similarity is used to measure alignment between resume and job description content.

---

### ATS Match Score Calculation
An ATS-style score is computed by comparing the semantic embeddings of the full resume and job description text.  
The similarity value is scaled to a percentage (0–100) to give users an intuitive understanding of resume–job fit.

---

### Keyword Matching and Gap Analysis
To provide actionable insights:
- Keywords present in both the resume and job description are identified as **matched**
- Relevant job description keywords missing from the resume are highlighted as **gaps**

This helps users improve resume alignment with ATS systems.

---

### Cover Letter Generation
The application automatically generates a clean, professional, and role-aware cover letter by:
- Extracting the job title from the job description
- Identifying semantically matched and partially matched skills
- Producing a concise, human-readable letter  

Users can preview the generated cover letter and download it as a PDF.

---

### Interactive Web Interface
All functionality is delivered through a Streamlit-based interface that allows users to upload files, view ATS scores, analyze keywords, and generate cover letters in a single workflow.

---

## Tech Stack
- Python  
- Natural Language Processing (Sentence Transformers)  
- Machine Learning  
- Streamlit  
- PyTorch  
- PDF and DOCX text extraction libraries  

---

## Demo
🔗 Live Demo: https://ai-resume-screener.streamlit.app

> **Note:**  
> The demo is hosted on a free-tier platform. If the application appears inactive or takes a few seconds to load, please refresh the page and allow time for the app to wake up.

---

## If the Demo Is Unavailable
If the live demo link is temporarily unavailable, the application can be run locally using the instructions below. All features remain fully accessible through local execution.

---

## Running the Project Locally

```bash
pip install -r requirements.txt
streamlit run app.py

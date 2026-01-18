from PyPDF2 import PdfReader
import docx2txt

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    try:
        pdf = PdfReader(file)
        return " ".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return f"[Error reading PDF: {e}]"

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    try:
        return docx2txt.process(file)
    except Exception as e:
        return f"[Error reading DOCX: {e}]"

def get_text(file):
    """Universal extractor for PDF/DOCX/TXT files."""
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

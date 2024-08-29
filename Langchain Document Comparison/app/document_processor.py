import PyPDF2
from io import BytesIO

def process_document(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return process_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return uploaded_file.getvalue().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def process_pdf(file):
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
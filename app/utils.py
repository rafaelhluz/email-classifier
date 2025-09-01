import pdfplumber
from fastapi import UploadFile

async def parse_pdf_text(file: UploadFile) -> str:
    """Extrai texto de um arquivo PDF."""
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Erro ao processar o arquivo PDF: {e}")
        return ""
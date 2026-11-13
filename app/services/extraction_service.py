from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_pdf(file_path: Path) -> list[dict]:
    reader = PdfReader(str(file_path))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            extracted_pages.append({
                "page_number": page_number,
                "text": text.strip(),
            })

    return extracted_pages


def extract_docx(file_path: Path) -> list[dict]:        # DOCX extraction here handles paragraphs, not tables; we'll address richer document structures if needed.
    document = Document(str(file_path))
 
    paragraphs = [
        text
        for paragraph in document.paragraphs
        if (text := paragraph.text.strip())
    ]

    text = "\n".join(paragraphs)

    return [{
        "page_number": None,
        "text": text,
    }] if text else []


def extract_txt(file_path: Path) -> list[dict]:
    text = file_path.read_text(encoding="utf-8-sig")

    text = text.strip()

    return [{
        "page_number": None,
        "text": text,
    }] if text else []


def extract_document(file_path: Path) -> list[dict]:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    if extension == ".txt":
        return extract_txt(file_path)

    raise ValueError("Unsupported document format")

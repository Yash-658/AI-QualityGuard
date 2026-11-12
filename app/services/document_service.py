from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile


UPLOAD_DIR = Path("data/uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024        # limits uploads to 10 MB.

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


async def save_document(file: UploadFile) -> dict:
    original_filename = file.filename or "unnamed"

    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload PDF, DOCX, or TXT files.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)         # reads at most one byte beyond the limit, allowing us to detect oversized uploads without loading an unlimited file into memory.

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum allowed size is 10 MB.",
        )

    document_id = str(uuid4())

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)        # creates the upload directory if it doesn't exist.

    stored_filename = f"{document_id}{file_extension}"
    file_path = UPLOAD_DIR / stored_filename

    file_path.write_bytes(content)

    return {
        "id": document_id,
        "filename": original_filename,
        "stored_filename": stored_filename,
        "size": len(content),
        "content_type": file.content_type,
    }

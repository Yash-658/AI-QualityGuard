from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.chunking_service import create_chunks
from app.services.document_service import save_document
from app.services.extraction_service import extract_document

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    document = await save_document(file)

    file_path = Path("data/uploads") / document["stored_filename"]

    try:
        extracted_pages = extract_document(file_path)
    except Exception as exc:                                # A failed extraction also currently leaves the uploaded file on disk; we'll improve cleanup when we build document lifecycle management.
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from the uploaded document.",
        ) from exc

    if not extracted_pages:
        raise HTTPException(
            status_code=422,
            detail="The document does not contain extractable text.",
        )
        
    chunks = create_chunks(
        extracted_pages=extracted_pages,
        document_id=document["id"],
        filename=document["filename"],
    )

    return {
        "message": "Document uploaded, extracted, and chunked successfully",
        "document": document,
        "extracted_pages": len(extracted_pages),
        "chunk_count": len(chunks),
    }

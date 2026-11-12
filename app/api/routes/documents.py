from fastapi import APIRouter, File, UploadFile

from app.services.document_service import save_document

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    document = await save_document(file)

    return {
        "message": "Document uploaded successfully",
        "document": document,
    }

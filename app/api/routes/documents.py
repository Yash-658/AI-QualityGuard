from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.services.document_service import save_document
from app.services.ingestion_service import DocumentIngestionService, get_ingestion_service


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: DocumentIngestionService = Depends(
        get_ingestion_service
    ),
):
    # Step 1: Save the uploaded document
    document = await save_document(file)

    file_path = Path("data/uploads") / document["stored_filename"]

    try:
        # Step 2: Execute the complete ingestion pipeline
        result = ingestion_service.process_document(
            file_path=file_path,
            document=document,
        )

    except ValueError as exc:
        file_path.unlink(missing_ok=True)       # This removes the file if it exists, without raising an error if it has already disappeared.

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the document.",
        ) from exc

    # Step 3: Return the processing summary
    return {
        "message": "Document successfully processed and stored",
        "document": document,
        **result,   #  placing ** before a dictionary unpacks its key-value pairs into separate keyword arguments
    }

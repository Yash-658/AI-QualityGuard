from functools import lru_cache
from pathlib import Path

from app.services.extraction_service import extract_document
from app.services.chunking_service import create_chunks
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


class DocumentIngestionService:          # keeps the orchestration logic separate from the HTTP layer.

    def __init__(self):                  # time expensive tasks done in the constructor itself, nd done only once during first api req
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def process_document(
        self,
        file_path: Path,
        document: dict,
    ) -> dict:

        # Step 1: Extract document text
        extracted_pages = extract_document(file_path)

        if not extracted_pages:
            raise ValueError(
                "The document does not contain extractable text."
            )

        # Step 2: Create chunks
        chunks = create_chunks(
            extracted_pages=extracted_pages,
            document_id=document["id"],
            filename=document["filename"],
        )

        if not chunks:
            raise ValueError(
                "No text chunks could be created from the document."
            )

        # Step 3: Generate embeddings
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.embedding_service.generate_embeddings(texts)

        # Step 4: Store chunks and embeddings
        self.vector_store.add_chunks(chunks, embeddings)

        return {
            "extracted_pages": len(extracted_pages),
            "chunk_count": len(chunks),
            "stored_chunks": len(chunks),
        }

# Reuse a single DocumentIngestionService instance across requests to save memory/setup time.

@lru_cache(maxsize=1)  # It caches the return values of a function.

def get_ingestion_service() -> DocumentIngestionService:
    return DocumentIngestionService()

import chromadb
import numpy as np
from chromadb.api.types import QueryResult
from pathlib import Path


CHROMA_PATH = Path("data/chroma")


class VectorStoreService:

    def __init__(self):
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
    ) -> None:

        if not chunks:
            return
        
        embedding_array = np.asarray(embeddings, dtype=np.float32)

        self.collection.add(
            ids=[chunk["chunk_id"] for chunk in chunks],
            embeddings=embedding_array,
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[
                {
                    "document_id": chunk["document_id"],
                    "filename": chunk["filename"],
                    "page_number": chunk["page_number"] or -1,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ) -> QueryResult:

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

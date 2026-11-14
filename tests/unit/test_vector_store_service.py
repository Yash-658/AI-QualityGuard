from app.services.vector_store_service import VectorStoreService

# tmp_path	Provides a temporary directory for test files and database storage.
# monkeypatch	Temporarily modifies variables or attributes during a test.

def test_add_and_search_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.services.vector_store_service.CHROMA_PATH",
        tmp_path / "chroma",
    )

    service = VectorStoreService()

    chunks = [
        {
            "chunk_id": "chunk-1",
            "document_id": "doc-1",
            "filename": "policy.pdf",
            "page_number": 1,
            "text": "Employees receive 20 days of annual leave.",
        }
    ]

    embeddings = [[0.1] * 384]

    service.add_chunks(chunks, embeddings)

    results = service.search(
        query_embedding=[0.1] * 384,
        n_results=1,
    )

    assert results["ids"] is not None
    assert results["documents"] is not None
    assert results["metadatas"] is not None

    assert results["ids"][0] == ["chunk-1"]
    assert results["documents"][0][0] == chunks[0]["text"]
    assert results["metadatas"][0][0]["document_id"] == chunks[0]["document_id"]
    assert results["metadatas"][0][0]["filename"] == chunks[0]["filename"]
    assert results["metadatas"][0][0]["page_number"] == chunks[0]["page_number"]


def test_add_empty_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.services.vector_store_service.CHROMA_PATH",
        tmp_path / "chroma",
    )

    service = VectorStoreService()

    service.add_chunks([], [])

    assert service.collection.count() == 0

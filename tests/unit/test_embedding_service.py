from app.services.embedding_service import EmbeddingService


def test_generate_embeddings():
    service = EmbeddingService()

    texts = [
        "Employees receive annual leave.",
        "The company provides health insurance.",
    ]

    embeddings = service.generate_embeddings(texts)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384


def test_generate_embeddings_with_empty_input():
    service = EmbeddingService()

    embeddings = service.generate_embeddings([])

    assert embeddings == []
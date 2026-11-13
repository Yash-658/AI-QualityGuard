from app.services.chunking_service import create_chunks


def test_create_chunks_from_long_text():
    words = [f"word{i}" for i in range(1100)]

    extracted_pages = [{
        "page_number": 1,
        "text": " ".join(words),
    }]

    chunks = create_chunks(
        extracted_pages=extracted_pages,
        document_id="doc-123",
        filename="sample.pdf",
    )

    assert len(chunks) == 3
    assert len(chunks[0]["text"].split()) == 500
    assert len(chunks[1]["text"].split()) == 500
    assert len(chunks[2]["text"].split()) == 200


def test_chunks_preserve_document_metadata():
    extracted_pages = [{
        "page_number": 3,
        "text": "This is a sample document.",
    }]

    chunks = create_chunks(
        extracted_pages=extracted_pages,
        document_id="doc-123",
        filename="sample.pdf",
    )

    assert chunks[0]["document_id"] == "doc-123"
    assert chunks[0]["filename"] == "sample.pdf"
    assert chunks[0]["page_number"] == 3


def test_empty_text_returns_no_chunks():
    extracted_pages = [{
        "page_number": 1,
        "text": "",
    }]

    chunks = create_chunks(
        extracted_pages=extracted_pages,
        document_id="doc-123",
        filename="sample.pdf",
    )

    assert chunks == []


def test_chunks_have_unique_ids():
    extracted_pages = [{
        "page_number": 1,
        "text": " ".join(["sample"] * 1100),
    }]

    chunks = create_chunks(
        extracted_pages=extracted_pages,
        document_id="doc-123",
        filename="sample.pdf",
    )

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))

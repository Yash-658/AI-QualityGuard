from uuid import uuid4


CHUNK_SIZE = 500                # I think its too high
CHUNK_OVERLAP = 50              # We do chunk overlapping in Retrieval-Augmented Generation (RAG) and text processing to prevent important information and context from being cut in half at the boundary of a chunk.


def create_chunks(
    extracted_pages: list[dict],
    document_id: str,
    filename: str,
) -> list[dict]:

    chunks = []

    for page in extracted_pages:
        text = page["text"]
        words = text.split()

        start = 0

        while start < len(words):
            end = start + CHUNK_SIZE

            chunk_words = words[start:end]          # start is inclusive, end is exclusive
            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():
                chunks.append({
                    "chunk_id": str(uuid4()),
                    "document_id": document_id,
                    "filename": filename,
                    "page_number": page["page_number"],
                    "text": chunk_text,
                })

            if end >= len(words):         # If end is larger than the list length, Python will not throw an error; it safely stops at the last available element.
                break

            start = end - CHUNK_OVERLAP

    return chunks


# important design decision: We are chunking each extracted PDF page independently. 
# This preserves accurate page citations and prevents a chunk from accidentally claiming to come from multiple pages. 
# DOCX and TXT are currently represented as one extracted text unit, so their chunks have no page number.
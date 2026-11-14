# AI-QualityGuard
AI-powered testing and quality automation framework for a RAG document assistant


>> Document/upload endpoint~
User uploads document
        |
        v
FastAPI receives request
        |
        v
Calls get_ingestion_service()
        |
        v
Checks lru_cache
        |
        +---- Cache empty?
        |       |
        |       v
        |   Create service
        |   Load model
        |   Initialize ChromaDB
        |   Cache instance
        |
        +---- Cache populated?
                |
                v
           Reuse instance
                |
                v
        Process uploaded document
from fastapi import FastAPI
from app.api.routes.documents import router as documents_router

app = FastAPI(
    title="AI-QualityGuard",
    description="AI-powered testing and quality automation framework for a RAG document assistant",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI-QualityGuard"
    }

app.include_router(documents_router)
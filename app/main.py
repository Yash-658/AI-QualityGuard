from fastapi import FastAPI
from app.api.routes.documents import router as documents_router
from app.services.ingestion_service import get_ingestion_service
from contextlib import asynccontextmanager

@asynccontextmanager     # Allows us to define startup and shutdown operations around the application's lifespan.
async def lifespan(app: FastAPI):
    # Startup: initialize ingestion services
    get_ingestion_service()

    yield

    # Shutdown: cleanup can be performed here if needed
    
    
app = FastAPI(
    title="AI-QualityGuard",
    description="AI-powered testing and quality automation framework for a RAG document assistant",
    version="0.1.0",
    lifespan=lifespan    # using eagerloading of time consuming tasks
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI-QualityGuard"
    }

app.include_router(documents_router)
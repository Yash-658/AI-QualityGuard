from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"   
      
# this model creates a vector with 384 dimensions~

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
    

# Performance note: Model loading can take time and download model files on the first run. 
# We'll make sure the model is initialized only once when we connect it to FastAPI, rather than loading it for every request.
from sentence_transformers import SentenceTransformer
from functools import lru_cache
from ..core.config import settings

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

def embed_text(text: str):
    model = get_model()
    return model.encode([text])[0]

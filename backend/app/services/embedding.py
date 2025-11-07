from functools import lru_cache
from ..core.config import settings

try:
    from sentence_transformers import SentenceTransformer
    has_sentence_transformers = True
except ImportError:
    has_sentence_transformers = False

@lru_cache(maxsize=1)
def get_model():
    if not has_sentence_transformers:
        return None
    return SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

def embed_text(text: str):
    model = get_model()
    if model is None:
        # Return a default embedding if model is not available
        return [0.0] * 384  # Default to 384-dimensional vector
    try:
        return model.encode([text])[0]
    except Exception:
        # Return a default embedding if encoding fails
        return [0.0] * 384

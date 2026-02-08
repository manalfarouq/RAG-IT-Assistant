"""Text embedding generation"""
from sentence_transformers import SentenceTransformer
import os

from ..core.config import settings

# Global model instance
_model = None


def get_model() -> SentenceTransformer:
    """
    Get or create embedding model (singleton pattern).
    
    Returns:
        Initialized SentenceTransformer model
    """
    global _model
    if _model is None:
        # Set HuggingFace token if available
        if settings.HF_TOKEN:
            os.environ['HUGGINGFACE_HUB_TOKEN'] = settings.HF_TOKEN
        
        _model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
            token=settings.HF_TOKEN,
            trust_remote_code=True
        )
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts.
    
    Args:
        texts: List of text strings
        
    Returns:
        List of embedding vectors
    """
    model = get_model()
    return model.encode(texts).tolist()


def embed_text(text: str) -> list[float]:
    """
    Generate embedding for a single text.
    
    Args:
        text: Text string
        
    Returns:
        Embedding vector
    """
    model = get_model()
    return model.encode([text])[0].tolist()


# Alias for compatibility
def get_embedding_model() -> SentenceTransformer:
    """Alias for get_model()"""
    return get_model()
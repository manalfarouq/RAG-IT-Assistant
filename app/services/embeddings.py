"""
Génération d'embeddings
"""
from sentence_transformers import SentenceTransformer
from ..core.config import settings
import os

# Définir le token HF comme variable d'environnement si disponible
if settings.HF_TOKEN:
    os.environ['HUGGINGFACE_HUB_TOKEN'] = settings.HF_TOKEN 

_model = None

def get_model():
    """Charge le modèle une seule fois"""
    global _model
    if _model is None:
        _model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
            token=settings.HF_TOKEN,
            trust_remote_code=True  # ← Ajouté
        )
    return _model

def get_embedding_model():
    """Retourne le modèle d'embeddings (pour clustering.py)"""
    return get_model()

def embed_texts(texts):
    """Génère des embeddings pour une liste de textes"""
    model = get_model()
    return model.encode(texts).tolist()

def embed_text(text):
    """Génère l'embedding pour UN SEUL texte"""
    model = get_model()
    return model.encode([text])[0].tolist()
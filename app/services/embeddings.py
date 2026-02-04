"""
Génération d'embeddings
"""
from sentence_transformers import SentenceTransformer
from core.config import settings

_model = None

def get_model():
    """Charge le modèle une seule fois"""
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def embed_texts(texts):
    """Génère des embeddings pour une liste de textes"""
    model = get_model()
    return model.encode(texts).tolist()

def embed_text(text):
    """Génère l'embedding pour UN SEUL texte"""
    model = get_model()
    return model.encode([text])[0].tolist()

# if __name__ == "__main__":
#     texts = [
#         "How to reset a Windows password?",
#         "Data backup procedure",
#         "New software installation",
#     ]

#     embeddings = embed_texts(texts)
#     print(f"Embeddings générés : {len(embeddings)}")
#     print(f"Dimension : {len(embeddings[0])}")
#     print(embeddings[2][:5])
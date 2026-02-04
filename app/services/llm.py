"""
Service LLM pour générer les réponses
"""
from transformers import pipeline
from core.config import settings

_llm = None

def get_llm():
    """Charge le modèle LLM une seule fois"""
    global _llm
    if _llm is None:
        _llm = pipeline(
            "text2text-generation",
            model=settings.LLM_MODEL,
            max_length=512
        )
    return _llm

def generate_answer(question, context):
    """
    Génère une réponse basée sur le contexte
    
    question: la question de l'utilisateur
    context: les chunks trouvés dans ChromaDB
    """
    llm = get_llm()
    
    # Construire le prompt
    prompt = f"""Contexte: {context}

Question: {question}

Réponds uniquement en te basant sur le contexte fourni. Si l'information n'est pas dans le contexte, dis "Je ne trouve pas cette information dans la documentation."

Réponse:"""
    
    # Générer la réponse
    result = llm(prompt, max_length=200, temperature=settings.LLM_TEMPERATURE)
    return result[0]['generated_text']  
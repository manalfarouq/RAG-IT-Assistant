"""
Service LLM pour générer les réponses
"""
from transformers import T5Tokenizer, T5ForConditionalGeneration
from ..core.config import settings

_tokenizer = None
_model = None

def get_llm():
    """Charge le modèle LLM une seule fois"""
    global _tokenizer, _model
    if _model is None:
        _tokenizer = T5Tokenizer.from_pretrained(settings.LLM_MODEL)
        _model = T5ForConditionalGeneration.from_pretrained(settings.LLM_MODEL)
    return _model, _tokenizer

def generate_answer(question, context):
    """
    Génère une réponse basée sur le contexte
    """
    model, tokenizer = get_llm()
    
    # Prompt simple pour T5
    prompt = f"question: {question} context: {context}"
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    
    # Générer
    outputs = model.generate(inputs.input_ids, max_length=200)
    
    # Décoder
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer if answer else "Aucune réponse trouvée."
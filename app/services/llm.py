"""
Service LLM pour générer les réponses - Gemini 2.5 Flash (Version améliorée)
"""
import logging
from google import genai
from google.genai import types
from ..core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------
# Configuration Gemini
# ---------------------------
logger.info("Configuration de Gemini 2.5 Flash...")
try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    logger.info("Gemini prêt!")
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation de Gemini: {e}")
    raise

# ---------------------------
# Constantes
# ---------------------------
MAX_ANSWER_LENGTH = 500  # longueur maximale de la réponse en caractères

# ---------------------------
# Fonction principale
# ---------------------------
def generate_answer(question: str, context: str, max_retries: int = 3) -> str:
    """
    Génère une réponse basée sur le contexte (RAG),
    avec fallback sur les bonnes pratiques IT si le contexte est insuffisant.

    Args:
        question: La question de l'utilisateur
        context: Le contexte extrait de la base de connaissances
        max_retries: Nombre maximum de tentatives en cas d'erreur

    Returns:
        str: La réponse générée
    """
    # Validation des entrées
    if not question or not question.strip():
        return "Erreur : Question vide."

    # Construction du prompt
    prompt = f"""Tu es un assistant professionnel de support IT spécialisé dans le troubleshooting et la formation des utilisateurs.

Contexte documentaire :
{context if context and context.strip() else "Aucun contexte spécifique n'a été trouvé dans la base de connaissances."}

Question de l'utilisateur :
{question}

Instructions :
1. Si le contexte contient des informations pertinentes, base ta réponse principalement dessus
2. Si le contexte est vide ou insuffisant, réponds en te basant sur les bonnes pratiques générales du support IT
3. Réponds de façon **brève et concise** (maximum {MAX_ANSWER_LENGTH} caractères)
4. Structure ta réponse de manière claire avec :
   - Une explication concise du concept ou problème
   - Des étapes pratiques si applicable
   - Des conseils ou précautions importantes
5. Utilise un ton professionnel mais accessible
6. N'invente jamais d'informations techniques non vérifiables
7. Si tu n'es pas certain, indique-le clairement

Réponds en français :"""

    # ---------------------------
    # Retry en cas d'erreur
    # ---------------------------
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    max_output_tokens=1024,
                    safety_settings=[
                        types.SafetySetting(
                            category="HARM_CATEGORY_DANGEROUS_CONTENT",
                            threshold="BLOCK_NONE"
                        )
                    ]
                )
            )

            # Extraction du texte et tronquage
            if response and response.text:
                answer = response.text.strip()
                if len(answer) > MAX_ANSWER_LENGTH:
                    # Tronquer sur la dernière phrase complète
                    answer = answer[:MAX_ANSWER_LENGTH].rsplit('.', 1)[0] + '.'
                logger.info(f"Réponse générée avec succès (tentative {attempt + 1})")
                return answer
            else:
                logger.warning(f"Réponse vide de Gemini (tentative {attempt + 1})")
                if attempt == max_retries - 1:
                    return "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer."

        except Exception as e:
            logger.error(f"Erreur génération Gemini (tentative {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                return f"Erreur lors de la génération de la réponse après {max_retries} tentatives. Veuillez contacter le support technique."

    return "Une erreur inattendue s'est produite."

"""LLM answer generation using Google Gemini"""
import logging
import google.generativeai as genai

from ..core.config import settings

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

MAX_ANSWER_LENGTH = 600


def generate_answer(question: str, context: str) -> str:
    """
    Generate answer using LLM with retrieved context.
    
    Args:
        question: User's question
        context: Retrieved context from vector store
        
    Returns:
        Generated answer or error message
    """
    if not context.strip():
        return f"I couldn't find relevant information for: '{question}'."
    
    prompt = f"""You are an IT support expert assistant based on "The IT Support Handbook" by Mike Halsey.

Context from the book (with page numbers):
{context}

Question: {question}

Instructions:
1. Answer ONLY based on the provided context
2. Cite page numbers when available
3. Be concise and practical (max {MAX_ANSWER_LENGTH} characters)
4. If context is insufficient, state this clearly
5. Focus on actionable information

Answer in English:"""

    try:
        logger.info("Calling Gemini API...")
        
        model = genai.GenerativeModel(settings.LLM_MODEL)
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                top_p=0.8,
                max_output_tokens=1024
            )
        )
        
        logger.info("Received Gemini response")
        
        if response and response.text:
            return response.text.strip()
        
        return "Sorry, I couldn't generate an answer."
    
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return f"LLM connection error.\n\nFound information:\n{context[:500]}..."
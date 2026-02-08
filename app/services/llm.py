"""Service LLM - Gemini"""
import logging
import google.generativeai as genai
from ..core.config import settings

logger = logging.getLogger(__name__)

# Configuration Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

MAX_ANSWER_LENGTH = 600

def generate_answer(question: str, context: str) -> str:
    """Génère une réponse basée sur le contexte RAG"""
    
    if not context.strip():
        return f"I couldn't find relevant information in my database for: '{question}'."
    
    # PROMPT PLUS FLEXIBLE
    prompt = f"""You are an IT support expert assistant based on "The IT Support Handbook" by Mike Halsey.

Context from the book (with page numbers):
{context}

Question: {question}

CRITICAL Instructions:
1. Answer ONLY based on the provided context
2. If the answer is in the context, cite the page numbers
3. Be concise and practical (max {MAX_ANSWER_LENGTH} characters)
4. If the context doesn't fully answer, say so clearly
5. Focus on actionable information

Answer in English:"""

    try:
        logger.info("🤖 Calling Gemini...")
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,  # ← Plus bas pour plus de précision
                top_p=0.8,
                max_output_tokens=1024
            )
        )
        
        logger.info("✅ Gemini response received")
        
        if response and response.text:
            return response.text.strip()
        
        return "Sorry, I couldn't generate an answer."
    
    except Exception as e:
        logger.error(f"❌ Gemini error: {e}")
        # Fallback avec contexte
        return f"⚠️ LLM connection error.\n\nFound information:\n{context[:500]}..."
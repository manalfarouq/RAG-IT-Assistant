"""
Pipeline RAG complet
"""
from ..services.vector_store import VectorStore
from ..services.llm import generate_answer

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
    
    def query(self, question, n_results=3):
        """
        Pipeline complet RAG
        
        1. Chercher les chunks pertinents dans ChromaDB
        2. Construire le contexte
        3. Envoyer au LLM
        4. Retourner la réponse
        """
        # 1. Recherche sémantique
        results = self.vector_store.search(question, n_results=n_results)
        
        # 2. Construire le contexte à partir des chunks trouvés
        context = "\n\n".join([r["document"] for r in results])
        
        # 3. Générer la réponse avec le LLM
        answer = generate_answer(question, context)
        
        # 4. Retourner la réponse (string, pas dict)
        return answer
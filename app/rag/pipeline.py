"""Pipeline RAG simplifié"""
from ..services.vector_store import VectorStore
from ..services.llm import generate_answer
from ..services.clustering import ClusteringService
import logging

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
        self.clustering = ClusteringService()
        logger.info("Pipeline RAG initialisé")

    def query(self, question: str, n_results: int = 30) -> tuple[str, str]:
        """Traite une question via RAG"""
        if not question.strip():
            return "Veuillez poser une question valide.", "Non classé"
        
        question = question.strip()
        cluster_id = self.clustering.assign_cluster(question)
        
        logger.info(f"🔍 Question: {question}")
        results = self.vector_store.search(question, n_results=n_results)
        
        if not results:
            logger.warning("❌ No results found")
            return (
                f"I couldn't find relevant information in my database for: '{question}'.",
                cluster_id
            )
        
        # Log des distances
        distances = [r['distance'] for r in results[:5]]
        logger.info(f"📏 Top 5 distances: {distances}")
        
        # FILTRER les résultats trop éloignés (mais garder au moins les 5 meilleurs)
        threshold = 1.2  # Seuil de distance
        filtered_results = [r for r in results if r['distance'] < threshold]
        
        # Si pas assez de résultats après filtrage, garde les 5 meilleurs
        if len(filtered_results) < 5:
            filtered_results = results[:5]
        
        logger.info(f"📊 Résultats gardés après filtrage : {len(filtered_results)}/{len(results)}")
        
        # Construction du contexte
        context_parts = []
        for r in filtered_results:
            if r.get("document"):
                metadata = r.get("metadata", {})
                page = metadata.get('page_number', 'N/A')
                context_parts.append(f"[Page {page}]\n{r['document']}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        logger.info(f"📄 Context length: {len(context)} chars")
        
        answer = generate_answer(question, context)
        return answer, cluster_id
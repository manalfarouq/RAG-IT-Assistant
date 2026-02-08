"""RAG pipeline for question answering"""
from ..services.vector_store import VectorStore
from ..services.llm import generate_answer
from ..services.clustering import ClusteringService
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline.
    
    Combines vector search, clustering, and LLM generation
    to answer IT support questions.
    """
    
    def __init__(self):
        """Initialize pipeline components"""
        self.vector_store = VectorStore()
        self.clustering = ClusteringService()
        logger.info("RAG pipeline initialized")

    def query(self, question: str, n_results: int = 30) -> tuple[str, str]:
        """
        Process a question through the RAG pipeline.
        
        Args:
            question: User's question
            n_results: Number of documents to retrieve
            
        Returns:
            Tuple of (answer, cluster_category)
        """
        if not question.strip():
            return "Please provide a valid question.", "Uncategorized"
        
        question = question.strip()
        cluster_id = self.clustering.assign_cluster(question)
        
        logger.info(f"Processing question: {question}")
        results = self.vector_store.search(question, n_results=n_results)
        
        if not results:
            logger.warning("No results found in vector store")
            return (
                f"I couldn't find relevant information for: '{question}'.",
                cluster_id
            )
        
        # Log search quality metrics
        distances = [r['distance'] for r in results[:5]]
        logger.info(f"Top 5 distances: {distances}")
        
        # Filter by distance threshold
        threshold = 1.2
        filtered_results = [r for r in results if r['distance'] < threshold]
        
        # Keep at least top 5 results
        if len(filtered_results) < 5:
            filtered_results = results[:5]
        
        logger.info(
            f"Results after filtering: {len(filtered_results)}/{len(results)}"
        )
        
        # Build context from retrieved documents
        context_parts = []
        for r in filtered_results:
            if r.get("document"):
                metadata = r.get("metadata", {})
                page = metadata.get('page_number', 'N/A')
                context_parts.append(f"[Page {page}]\n{r['document']}")
        
        context = "\n\n---\n\n".join(context_parts)
        logger.info(f"Context length: {len(context)} characters")
        
        # Generate answer using LLM
        answer = generate_answer(question, context)
        return answer, cluster_id
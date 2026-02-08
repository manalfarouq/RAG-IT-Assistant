"""
Pipeline RAG complet (Version améliorée)
"""
from ..services.vector_store import VectorStore
from ..services.llm import generate_answer
from ..services.clustering import ClusteringService
import logging

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        """Initialise le pipeline RAG avec gestion d'erreurs"""
        try:
            self.vector_store = VectorStore()
            self.clustering = ClusteringService()
            logger.info("Pipeline RAG initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du pipeline RAG: {e}")
            raise

    def query(self, question: str, n_results: int = 3) -> tuple[str, str]:
        """
        Traite une question utilisateur via le pipeline RAG complet
        
        Args:
            question: La question de l'utilisateur
            n_results: Nombre de résultats à récupérer du vector store
            
        Returns:
            tuple: (réponse générée, cluster_id)
        """
        try:
            # Validation de l'entrée
            if not question or not question.strip():
                logger.warning("Question vide reçue")
                return "Veuillez poser une question valide.", "Non classé"
            
            question = question.strip()
            logger.info(f"Traitement de la question: {question[:100]}...")
            
            # 1️⃣ Clustering avec gestion d'erreur
            try:
                cluster_id = self.clustering.assign_cluster(question)
                logger.info(f"Question assignée au cluster: {cluster_id}")
            except Exception as e:
                logger.error(f"Erreur clustering: {e}")
                cluster_id = "Non classé"
            
            # 2️⃣ Recherche vectorielle avec gestion d'erreur
            try:
                results = self.vector_store.search(question, n_results=n_results)
                logger.info(f"Recherche vectorielle: {len(results)} résultats trouvés")
            except Exception as e:
                logger.error(f"Erreur recherche vectorielle: {e}")
                results = []
            
            # 3️⃣ Construction du contexte
            if not results:
                logger.warning("Aucun contexte trouvé dans la base vectorielle")
                context = ""
            else:
                context_parts = []
                for i, r in enumerate(results):
                    if r.get("document"):
                        # Ajout de métadonnées pour améliorer le contexte
                        score = r.get("score", 0)
                        context_parts.append(
                            f"[Pertinence: {score:.2f}]\n{r['document']}"
                        )
                
                context = "\n\n---\n\n".join(context_parts)
                
                # Log du contexte (tronqué pour la lisibilité)
                logger.debug(f"Contexte construit ({len(context)} caractères)")
                if len(context) > 500:
                    logger.debug(f"Aperçu: {context[:500]}...")
                else:
                    logger.debug(f"Contexte complet: {context}")
            
            # 4️⃣ Génération de la réponse avec gestion d'erreur
            try:
                answer = generate_answer(question, context)
                logger.info("Réponse générée avec succès")
            except Exception as e:
                logger.error(f"Erreur génération réponse: {e}")
                answer = (
                    "Désolé, une erreur s'est produite lors de la génération de la réponse. "
                    "Veuillez réessayer ou contacter le support technique."
                )
            
            return answer, cluster_id
            
        except Exception as e:
            logger.error(f"Erreur critique dans le pipeline RAG: {e}", exc_info=True)
            return (
                "Une erreur inattendue s'est produite. Veuillez réessayer ultérieurement.",
                "Erreur"
            )
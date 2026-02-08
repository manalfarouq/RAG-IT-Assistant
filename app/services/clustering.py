"""Service de clustering"""
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import logging

from .embeddings import embed_text, embed_texts
from ..scripts.questions import questions, questions_data

logger = logging.getLogger(__name__)

class ClusteringService:
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)
        
        # Mapping question -> catégorie
        self.question_to_category = {
            q["question"]: q["category"] for q in questions_data
        }
        
        self._initialize()
    
    def _initialize(self):
        """Initialise le clustering"""
        if not questions:
            logger.warning("Aucune question de référence")
            return
        
        # Génération embeddings
        embeddings = np.array(embed_texts(questions))
        
        # Fit
        self.kmeans.fit(embeddings)
        
        # Cache
        self._reference_embeddings = embeddings
        self._reference_clusters = self.kmeans.predict(embeddings)
        
        logger.info(f"Clustering initialisé avec {len(questions)} questions")
    
    def assign_cluster(self, question: str) -> str:
        """Assigne une catégorie à une question"""
        if not question.strip():
            return "Non classé"
        
        question = question.strip()
        
        # Si question de référence exacte
        if question in self.question_to_category:
            return self.question_to_category[question]
        
        # Prédiction
        embedding = np.array([embed_text(question)])
        cluster_id = self.kmeans.predict(embedding)[0]
        
        # Mise à jour incrémentale
        self.kmeans.partial_fit(embedding)
        
        # Trouver catégorie
        return self._find_category_for_cluster(cluster_id)
    
    def _find_category_for_cluster(self, cluster_id: int) -> str:
        """Trouve la catégorie majoritaire d'un cluster"""
        matching_indices = np.where(self._reference_clusters == cluster_id)[0]
        
        if len(matching_indices) == 0:
            return f"Cluster_{cluster_id}"
        
        # Compter catégories
        category_counts = {}
        for idx in matching_indices:
            question = questions[idx]
            category = self.question_to_category.get(question, "Non classé")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Retourner majoritaire
        return max(category_counts, key=category_counts.get) if category_counts else f"Cluster_{cluster_id}"
"""
Service de clustering amélioré avec gestion d'erreurs
"""
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import logging
from typing import Optional

from .embeddings import embed_text, embed_texts
from ..scripts.questions import questions, questions_data

logger = logging.getLogger(__name__)

class ClusteringService:
    def __init__(self, n_clusters: int = 5):
        """
        Initialise le service de clustering
        
        Args:
            n_clusters: Nombre de clusters à créer
        """
        self.n_clusters = n_clusters
        self.kmeans = MiniBatchKMeans(
            n_clusters=n_clusters,
            random_state=42,
            batch_size=100,
            max_iter=100
        )
        self.fitted = False
        
        # Mapping question -> catégorie
        self.question_to_category = {
            q["question"]: q["category"] for q in questions_data
        }
        
        # Cache pour les embeddings des questions de référence
        self._reference_embeddings = None
        self._reference_clusters = None
        
        self._initialize()
    
    def _initialize(self):
        """Initialise le clustering avec les questions de base"""
        try:
            if not questions:
                logger.warning("Aucune question de référence disponible")
                return
            
            logger.info(f"Initialisation du clustering avec {len(questions)} questions...")
            
            # Générer les embeddings
            embeddings = embed_texts(questions)
            
            if embeddings is None or len(embeddings) == 0:
                logger.error("Échec de génération des embeddings")
                return
            
            # Vérifier la dimensionnalité
            embeddings_array = np.array(embeddings)
            logger.info(f"Shape des embeddings: {embeddings_array.shape}")
            
            # Fit du modèle
            self.kmeans.fit(embeddings_array)
            self.fitted = True
            
            # Cache des embeddings et clusters de référence
            self._reference_embeddings = embeddings_array
            self._reference_clusters = self.kmeans.predict(embeddings_array)
            
            # Log de la distribution des clusters
            unique, counts = np.unique(self._reference_clusters, return_counts=True)
            cluster_dist = dict(zip(unique, counts))
            logger.info(f"Clustering initialisé - Distribution: {cluster_dist}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du clustering: {e}", exc_info=True)
            self.fitted = False
    
    def assign_cluster(self, question: str) -> str:
        """
        Assigne une catégorie à une question
        
        Args:
            question: La question à classifier
            
        Returns:
            str: La catégorie assignée
        """
        try:
            # Validation
            if not question or not question.strip():
                logger.warning("Question vide pour le clustering")
                return "Non classé"
            
            question = question.strip()
            
            # Si c'est une question de référence exacte, retour direct
            if question in self.question_to_category:
                category = self.question_to_category[question]
                logger.debug(f"Question de référence trouvée: {category}")
                return category
            
            # Si le clustering n'est pas initialisé
            if not self.fitted:
                logger.warning("Clustering non initialisé")
                return "Non classé"
            
            # Génération de l'embedding pour la nouvelle question
            try:
                embedding = embed_text(question)
                if embedding is None:
                    logger.error("Échec de génération de l'embedding")
                    return "Non classé"
                
                # Reshape pour sklearn
                embedding_array = np.array([embedding])
                
            except Exception as e:
                logger.error(f"Erreur génération embedding: {e}")
                return "Non classé"
            
            # Prédiction du cluster
            try:
                cluster_id = self.kmeans.predict(embedding_array)[0]
                logger.debug(f"Question assignée au cluster {cluster_id}")
            except Exception as e:
                logger.error(f"Erreur prédiction cluster: {e}")
                return "Non classé"
            
            # Mise à jour incrémentale du modèle
            try:
                self.kmeans.partial_fit(embedding_array)
            except Exception as e:
                logger.warning(f"Échec partial_fit (non critique): {e}")
            
            # Trouver la catégorie du cluster via les questions de référence
            try:
                category = self._find_category_for_cluster(cluster_id)
                logger.debug(f"Catégorie trouvée: {category}")
                return category
            except Exception as e:
                logger.error(f"Erreur recherche catégorie: {e}")
                return f"Cluster_{cluster_id}"
            
        except Exception as e:
            logger.error(f"Erreur inattendue dans assign_cluster: {e}", exc_info=True)
            return "Erreur"
    
    def _find_category_for_cluster(self, cluster_id: int) -> str:
        """
        Trouve la catégorie majoritaire pour un cluster donné
        
        Args:
            cluster_id: L'ID du cluster
            
        Returns:
            str: La catégorie la plus représentative
        """
        if self._reference_clusters is None:
            return f"Cluster_{cluster_id}"
        
        # Trouver toutes les questions du même cluster
        matching_indices = np.where(self._reference_clusters == cluster_id)[0]
        
        if len(matching_indices) == 0:
            return f"Cluster_{cluster_id}"
        
        # Compter les catégories dans ce cluster
        category_counts = {}
        for idx in matching_indices:
            if idx < len(questions):
                question = questions[idx]
                category = self.question_to_category.get(question, "Non classé")
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Retourner la catégorie majoritaire
        if category_counts:
            majority_category = max(category_counts, key=category_counts.get)
            logger.debug(f"Cluster {cluster_id} -> {majority_category} (sur {category_counts})")
            return majority_category
        
        return f"Cluster_{cluster_id}"
    
    def get_cluster_info(self) -> dict:
        """
        Retourne des informations sur l'état du clustering
        
        Returns:
            dict: Informations de diagnostic
        """
        if not self.fitted:
            return {
                "status": "not_initialized",
                "n_clusters": self.n_clusters,
                "n_questions": len(questions)
            }
        
        cluster_distribution = {}
        if self._reference_clusters is not None:
            unique, counts = np.unique(self._reference_clusters, return_counts=True)
            cluster_distribution = {int(k): int(v) for k, v in zip(unique, counts)}
        
        return {
            "status": "initialized",
            "n_clusters": self.n_clusters,
            "n_questions": len(questions),
            "cluster_distribution": cluster_distribution,
            "n_categories": len(set(self.question_to_category.values()))
        }
"""Question clustering service"""
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import logging

from .embeddings import embed_text, embed_texts
from ..scripts.questions import questions, questions_data

logger = logging.getLogger(__name__)


class ClusteringService:
    """
    K-Means clustering for question categorization.
    
    Automatically assigns questions to predefined categories
    based on semantic similarity.
    """
    
    def __init__(self, n_clusters: int = 5):
        """
        Initialize clustering model.
        
        Args:
            n_clusters: Number of clusters to create
        """
        self.n_clusters = n_clusters
        self.kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)
        
        # Map questions to categories
        self.question_to_category = {
            q["question"]: q["category"] for q in questions_data
        }
        
        self._initialize()
    
    def _initialize(self):
        """Train clustering model on reference questions"""
        if not questions:
            logger.warning("No reference questions available")
            return
        
        # Generate embeddings
        embeddings = np.array(embed_texts(questions))
        
        # Train model
        self.kmeans.fit(embeddings)
        
        # Cache predictions
        self._reference_embeddings = embeddings
        self._reference_clusters = self.kmeans.predict(embeddings)
        
        logger.info(f"Clustering initialized with {len(questions)} questions")
    
    def assign_cluster(self, question: str) -> str:
        """
        Assign a category to a question.
        
        Args:
            question: Question to categorize
            
        Returns:
            Category name or cluster ID
        """
        if not question.strip():
            return "Uncategorized"
        
        question = question.strip()
        
        # Check for exact match
        if question in self.question_to_category:
            return self.question_to_category[question]
        
        # Predict cluster
        embedding = np.array([embed_text(question)])
        cluster_id = self.kmeans.predict(embedding)[0]
        
        # Update model incrementally
        self.kmeans.partial_fit(embedding)
        
        # Find category
        return self._find_category_for_cluster(cluster_id)
    
    def _find_category_for_cluster(self, cluster_id: int) -> str:
        """
        Find most common category in a cluster.
        
        Args:
            cluster_id: Cluster identifier
            
        Returns:
            Most common category name
        """
        matching_indices = np.where(self._reference_clusters == cluster_id)[0]
        
        if len(matching_indices) == 0:
            return f"Cluster_{cluster_id}"
        
        # Count categories
        category_counts = {}
        for idx in matching_indices:
            question = questions[idx]
            category = self.question_to_category.get(question, "Uncategorized")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Return most common
        return max(category_counts, key=category_counts.get) if category_counts else f"Cluster_{cluster_id}"
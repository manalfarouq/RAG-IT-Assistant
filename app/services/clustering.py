"""
Service de clustering des questions avec K-Means
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple, Optional
import pickle
import os
from pathlib import Path

from services.embeddings import get_embedding_model
from core.config import settings


class QuestionClusterer:
    """Classe pour gérer le clustering des questions"""
    
    def __init__(self, n_clusters: int = 5):
        """
        Initialise le clusterer
        
        Args:
            n_clusters: Nombre de clusters à créer
        """
        self.n_clusters = n_clusters
        self.embedding_model = get_embedding_model()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.is_fitted = False
        
        # Chemin pour sauvegarder le modèle
        self.model_dir = Path("data/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.model_path = self.model_dir / "question_clusterer.pkl"
    
    def embed_questions(self, questions: List[str]) -> np.ndarray:
        """
        Génère les embeddings pour une liste de questions
        
        Args:
            questions: Liste des questions
            
        Returns:
            Array numpy des embeddings
        """
        embeddings = []
        for question in questions:
            embedding = self.embedding_model.embed_query(question)
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def fit(self, questions: List[str]) -> None:
        """
        Entraîne le modèle de clustering
        
        Args:
            questions: Liste des questions pour l'entraînement
        """
        if len(questions) < self.n_clusters:
            raise ValueError(
                f"Le nombre de questions ({len(questions)}) doit être >= "
                f"au nombre de clusters ({self.n_clusters})"
            )
        
        # Générer les embeddings
        print(f"Génération des embeddings pour {len(questions)} questions...")
        embeddings = self.embed_questions(questions)
        
        # Normaliser les embeddings
        embeddings_scaled = self.scaler.fit_transform(embeddings)
        
        # Entraîner K-Means
        print(f"Entraînement du clustering avec {self.n_clusters} clusters...")
        self.kmeans.fit(embeddings_scaled)
        self.is_fitted = True
        
        print(f"Clustering terminé. Inertie: {self.kmeans.inertia_:.2f}")
    
    def predict(self, question: str) -> int:
        """
        Prédit le cluster d'une question
        
        Args:
            question: Question à classifier
            
        Returns:
            Numéro du cluster (0 à n_clusters-1)
        """
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné avant la prédiction")
        
        # Générer l'embedding
        embedding = self.embedding_model.embed_query(question)
        embedding = np.array([embedding])
        
        # Normaliser
        embedding_scaled = self.scaler.transform(embedding)
        
        # Prédire le cluster
        cluster = self.kmeans.predict(embedding_scaled)[0]
        
        return int(cluster)
    
    def predict_batch(self, questions: List[str]) -> List[int]:
        """
        Prédit les clusters pour plusieurs questions
        
        Args:
            questions: Liste des questions
            
        Returns:
            Liste des numéros de clusters
        """
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné avant la prédiction")
        
        # Générer les embeddings
        embeddings = self.embed_questions(questions)
        
        # Normaliser
        embeddings_scaled = self.scaler.transform(embeddings)
        
        # Prédire les clusters
        clusters = self.kmeans.predict(embeddings_scaled)
        
        return clusters.tolist()
    
    def get_cluster_centers(self) -> np.ndarray:
        """
        Retourne les centres des clusters
        
        Returns:
            Array numpy des centres de clusters
        """
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné")
        
        return self.kmeans.cluster_centers_
    
    def save_model(self) -> None:
        """Sauvegarde le modèle entraîné"""
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné avant la sauvegarde")
        
        model_data = {
            'kmeans': self.kmeans,
            'scaler': self.scaler,
            'n_clusters': self.n_clusters,
            'is_fitted': self.is_fitted
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Modèle sauvegardé dans {self.model_path}")
    
    def load_model(self) -> bool:
        """
        Charge un modèle sauvegardé
        
        Returns:
            True si le chargement a réussi, False sinon
        """
        if not self.model_path.exists():
            print(f"Aucun modèle trouvé dans {self.model_path}")
            return False
        
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.kmeans = model_data['kmeans']
            self.scaler = model_data['scaler']
            self.n_clusters = model_data['n_clusters']
            self.is_fitted = model_data['is_fitted']
            
            print(f"Modèle chargé depuis {self.model_path}")
            return True
        
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            return False
    
    def get_cluster_statistics(self, questions: List[str], labels: List[int]) -> dict:
        """
        Calcule des statistiques sur les clusters
        
        Args:
            questions: Liste des questions
            labels: Liste des labels de clusters
            
        Returns:
            Dictionnaire avec les statistiques
        """
        stats = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_questions = [q for q, l in zip(questions, labels) if l == cluster_id]
            stats[f"cluster_{cluster_id}"] = {
                "count": len(cluster_questions),
                "percentage": len(cluster_questions) / len(questions) * 100,
                "sample_questions": cluster_questions[:3]  # 3 exemples
            }
        
        return stats


# Instance globale du clusterer
_clusterer: Optional[QuestionClusterer] = None


def get_question_clusterer(n_clusters: int = 5) -> QuestionClusterer:
    """
    Retourne l'instance globale du clusterer (singleton)
    
    Args:
        n_clusters: Nombre de clusters
        
    Returns:
        Instance de QuestionClusterer
    """
    global _clusterer
    
    if _clusterer is None:
        _clusterer = QuestionClusterer(n_clusters=n_clusters)
        # Tenter de charger un modèle existant
        _clusterer.load_model()
    
    return _clusterer
"""
Script pour visualiser les clusters de questions
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

# Ajouter le dossier app au path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.query_model import Query
from services.clustering import get_question_clusterer


def visualize_clusters():
    """Visualise les clusters de questions en 2D"""
    
    print("=" * 60)
    print("VISUALISATION DES CLUSTERS")
    print("=" * 60)
    
    # Connexion à la base de données
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Récupérer les questions
        queries = db.query(Query).filter(Query.cluster.isnot(None)).all()
        
        if not queries:
            print("Aucune question avec cluster trouvée")
            return
        
        print(f"\nQuestions trouvées: {len(queries)}")
        
        # Extraire questions et labels
        questions = [q.question for q in queries]
        labels = [q.cluster for q in queries]
        
        # Obtenir le clusterer
        clusterer = get_question_clusterer()
        
        if not clusterer.load_model():
            print("Impossible de charger le modèle")
            return
        
        # Générer les embeddings
        print("\nGénération des embeddings...")
        embeddings = clusterer.embed_questions(questions)
        
        # Réduire à 2D avec PCA
        print("Réduction dimensionnelle (PCA)...")
        pca = PCA(n_components=2)
        embeddings_2d = pca.fit_transform(embeddings)
        
        # Créer le graphique
        print("Création du graphique...")
        plt.figure(figsize=(12, 8))
        
        # Couleurs pour chaque cluster
        colors = plt.cm.rainbow(np.linspace(0, 1, clusterer.n_clusters))
        
        for cluster_id in range(clusterer.n_clusters):
            # Points du cluster
            mask = np.array(labels) == cluster_id
            cluster_points = embeddings_2d[mask]
            
            if len(cluster_points) > 0:
                plt.scatter(
                    cluster_points[:, 0],
                    cluster_points[:, 1],
                    c=[colors[cluster_id]],
                    label=f'Cluster {cluster_id} ({np.sum(mask)} questions)',
                    alpha=0.6,
                    s=100
                )
        
        # Centres des clusters (projetés en 2D)
        centers = clusterer.get_cluster_centers()
        centers_2d = pca.transform(centers)
        
        plt.scatter(
            centers_2d[:, 0],
            centers_2d[:, 1],
            c='black',
            marker='X',
            s=300,
            label='Centres',
            edgecolors='white',
            linewidths=2
        )
        
        plt.xlabel('Composante principale 1')
        plt.ylabel('Composante principale 2')
        plt.title('Visualisation des Clusters de Questions (PCA 2D)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Sauvegarder
        output_path = Path("data/clusters_visualization.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nGraphique sauvegardé: {output_path}")
        
        # Afficher
        plt.show()
        
        # Afficher les statistiques
        print("\nStatistiques:")
        print("-" * 60)
        for cluster_id in range(clusterer.n_clusters):
            count = sum(1 for l in labels if l == cluster_id)
            percentage = (count / len(labels)) * 100
            print(f"Cluster {cluster_id}: {count} questions ({percentage:.1f}%)")
        
        print("\n" + "=" * 60)
    
    except Exception as e:
        print(f"\nErreur: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    visualize_clusters()
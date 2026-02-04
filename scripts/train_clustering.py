"""
Script pour entraîner le modèle de clustering sur les questions existantes
"""
import sys
from pathlib import Path

# Ajouter le dossier app au path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.query_model import Query
from services.clustering import get_question_clusterer


def train_clustering_model(n_clusters: int = 5, min_questions: int = 10):
    """
    Entraîne le modèle de clustering sur les questions en base
    
    Args:
        n_clusters: Nombre de clusters à créer
        min_questions: Nombre minimum de questions requises
    """
    print("=" * 60)
    print("ENTRAÎNEMENT DU MODÈLE DE CLUSTERING")
    print("=" * 60)
    
    # Connexion à la base de données
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Récupérer toutes les questions
        queries = db.query(Query).all()
        questions = [q.question for q in queries]
        
        print(f"\nQuestions trouvées: {len(questions)}")
        
        if len(questions) < min_questions:
            print(f"Pas assez de questions pour le clustering")
            print(f"   Minimum requis: {min_questions}, trouvé: {len(questions)}")
            return
        
        if len(questions) < n_clusters:
            print(f"Ajustement du nombre de clusters: {n_clusters} → {len(questions)}")
            n_clusters = max(2, len(questions) // 2)
        
        # Obtenir le clusterer
        clusterer = get_question_clusterer(n_clusters=n_clusters)
        
        # Entraîner le modèle
        print(f"\nEntraînement en cours...")
        clusterer.fit(questions)
        
        # Prédire les clusters pour toutes les questions
        print(f"\nPrédiction des clusters...")
        labels = clusterer.predict_batch(questions)
        
        # Calculer les statistiques
        stats = clusterer.get_cluster_statistics(questions, labels)
        
        print(f"\nStatistiques des clusters:")
        print("-" * 60)
        for cluster_name, cluster_stats in stats.items():
            print(f"\n{cluster_name.upper()}:")
            print(f"  • Nombre de questions: {cluster_stats['count']}")
            print(f"  • Pourcentage: {cluster_stats['percentage']:.1f}%")
            print(f"  • Exemples:")
            for i, q in enumerate(cluster_stats['sample_questions'], 1):
                print(f"    {i}. {q[:80]}...")
        
        # Mettre à jour les clusters dans la base de données
        print(f"\nMise à jour de la base de données...")
        for query, label in zip(queries, labels):
            query.cluster = label
        
        db.commit()
        print(f"✅ {len(queries)} questions mises à jour")
        
        # Sauvegarder le modèle
        print(f"\nSauvegarde du modèle...")
        clusterer.save_model()
        
        print(f"\n✅ Entraînement terminé avec succès!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Entraîner le modèle de clustering")
    parser.add_argument(
        "--n-clusters",
        type=int,
        default=5,
        help="Nombre de clusters (défaut: 5)"
    )
    parser.add_argument(
        "--min-questions",
        type=int,
        default=10,
        help="Nombre minimum de questions requises (défaut: 10)"
    )
    
    args = parser.parse_args()
    
    train_clustering_model(
        n_clusters=args.n_clusters,
        min_questions=args.min_questions
    )
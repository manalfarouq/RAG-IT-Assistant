"""
Route pour les requêtes RAG avec clustering
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import time

from db.database import get_db
from auth.token_auth import get_current_user
from schemas.Query_schema import QueryRequest, QueryResponse
from models.query_model import Query
from models.user_model import User
from rag.pipeline import RAGPipeline
from services.clustering import get_question_clusterer


router = APIRouter(prefix="/query", tags=["RAG Query"])

# Instance globale du pipeline RAG
rag_pipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """Retourne l'instance du pipeline RAG (singleton)"""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline


@router.post("/", response_model=QueryResponse)
async def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Effectue une requête RAG avec clustering automatique
    
    - Recherche dans la base de connaissances
    - Génère une réponse
    - Assigne automatiquement à un cluster
    - Enregistre la requête en base
    """
    try:
        # Mesurer le temps de latence
        start_time = time.time()
        
        # Obtenir le pipeline RAG
        pipeline = get_rag_pipeline()
        
        # Générer la réponse
        answer = pipeline.query(request.question)
        
        # Prédire le cluster de la question
        clusterer = get_question_clusterer()
        cluster_id = None
        
        if clusterer.is_fitted:
            try:
                cluster_id = clusterer.predict(request.question)
            except Exception as e:
                print(f"Erreur lors de la prédiction du cluster: {e}")
                # Continuer sans cluster si erreur
        
        # Calculer la latence
        latency_ms = (time.time() - start_time) * 1000
        
        # Créer l'entrée en base de données
        new_query = Query(
            user_id=current_user_id,
            question=request.question,
            answer=answer,
            cluster=cluster_id,
            latency_ms=latency_ms,
            created_at=datetime.utcnow()
        )
        
        db.add(new_query)
        db.commit()
        db.refresh(new_query)
        
        return new_query
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement de la requête: {str(e)}"
        )


@router.get("/clusters/stats")
async def get_cluster_stats(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Retourne les statistiques des clusters pour l'utilisateur actuel
    """
    queries = db.query(Query).filter(Query.user_id == current_user_id).all()
    
    if not queries:
        return {"message": "Aucune requête trouvée"}
    
    # Compter les questions par cluster
    cluster_counts = {}
    for query in queries:
        if query.cluster is not None:
            cluster_counts[query.cluster] = cluster_counts.get(query.cluster, 0) + 1
    
    # Calculer les statistiques
    total_queries = len(queries)
    clustered_queries = sum(cluster_counts.values())
    
    stats = {
        "total_queries": total_queries,
        "clustered_queries": clustered_queries,
        "unclustered_queries": total_queries - clustered_queries,
        "clusters": {}
    }
    
    for cluster_id, count in cluster_counts.items():
        # Récupérer des exemples de questions du cluster
        cluster_queries = [
            q for q in queries 
            if q.cluster == cluster_id
        ][:3]  # 3 exemples
        
        stats["clusters"][f"cluster_{cluster_id}"] = {
            "count": count,
            "percentage": (count / total_queries) * 100,
            "sample_questions": [q.question for q in cluster_queries]
        }
    
    return stats


@router.get("/clusters/{cluster_id}")
async def get_cluster_questions(
    cluster_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
    limit: int = 50
):
    """
    Retourne toutes les questions d'un cluster spécifique
    """
    queries = (
        db.query(Query)
        .filter(
            Query.user_id == current_user_id,
            Query.cluster == cluster_id
        )
        .order_by(Query.created_at.desc())
        .limit(limit)
        .all()
    )
    
    return {
        "cluster_id": cluster_id,
        "count": len(queries),
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "answer": q.answer,
                "created_at": q.created_at
            }
            for q in queries
        ]
    }


@router.post("/retrain-clusters")
async def retrain_clusters(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
    n_clusters: int = 5
):
    """
    Réentraîne le modèle de clustering (admin uniquement dans une vraie app)
    """
    try:
        # Récupérer toutes les questions
        queries = db.query(Query).all()
        questions = [q.question for q in queries]
        
        if len(questions) < n_clusters:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pas assez de questions. Minimum: {n_clusters}, trouvé: {len(questions)}"
            )
        
        # Obtenir le clusterer
        clusterer = get_question_clusterer(n_clusters=n_clusters)
        
        # Entraîner
        clusterer.fit(questions)
        
        # Prédire les nouveaux clusters
        labels = clusterer.predict_batch(questions)
        
        # Mettre à jour la base
        for query, label in zip(queries, labels):
            query.cluster = label
        
        db.commit()
        
        # Sauvegarder le modèle
        clusterer.save_model()
        
        return {
            "message": "Clustering réentraîné avec succès",
            "n_questions": len(questions),
            "n_clusters": n_clusters
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du réentraînement: {str(e)}"
        )
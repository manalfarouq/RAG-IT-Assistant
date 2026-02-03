"""
Route pour interroger le RAG
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import time

from app.db.database import get_db
from app.models.query_model import Query
from app.models.user_model import User
from app.schemas.query_schema import QueryRequest, QueryResponse
from app.rag.pipeline import RAGPipeline
from app.api.auth.token_auth import get_current_user


router = APIRouter(prefix="/query", tags=["RAG Query"])

# Instance unique du pipeline RAG
rag_pipeline = RAGPipeline()


@router.post("/", response_model=QueryResponse)
def ask_question(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Poser une question au RAG
    
    - Authentification requise
    - Mesure le temps de réponse (latency)
    - Sauvegarde dans PostgreSQL
    """
    # Mesurer le temps de début
    start_time = time.time()
    
    try:
        # Interroger le RAG
        result = rag_pipeline.query(
            question=request.question,
            n_results=request.n_results
        )
        
        # Calculer la latence en millisecondes
        latency_ms = (time.time() - start_time) * 1000
        
        # Créer l'entrée dans la DB
        query = Query(
            user_id=current_user.id,
            question=request.question,
            answer=result["answer"],
            latency_ms=latency_ms
        )
        
        db.add(query)
        db.commit()
        db.refresh(query)
        
        return query
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération de la réponse: {str(e)}"
        )
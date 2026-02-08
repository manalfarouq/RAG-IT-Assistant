"""Route pour les requêtes RAG"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import time

from ..db.database import get_db
from ..auth.token_auth import get_current_user
from ..schemas.query_schema import QueryRequest, QueryResponse
from ..models.query_model import Query
from ..rag.pipeline import RAGPipeline

router = APIRouter(prefix="/query", tags=["RAG Query"])

# Instance unique du pipeline
rag_pipeline = RAGPipeline()


@router.post("/", response_model=QueryResponse)
def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Effectue une requête RAG"""
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La question ne peut pas être vide"
        )
    
    start_time = time.time()
    
    # Exécution RAG
    answer, cluster_id = rag_pipeline.query(request.question)
    
    # Calcul latence
    latency_ms = (time.time() - start_time) * 1000
    
    # Sauvegarde
    new_query = Query(
        user_id=current_user_id,
        question=request.question.strip(),
        answer=answer,
        cluster=cluster_id,
        latency_ms=round(latency_ms, 2),
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    
    return new_query


@router.get("/health")
def health_check():
    """Vérifie que le service est opérationnel"""
    return {
        "status": "healthy",
        "service": "RAG Query"
    }
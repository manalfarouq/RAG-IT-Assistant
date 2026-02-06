"""
Route pour les requêtes RAG
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import time

from ..db.database import get_db
from ..auth.token_auth import get_current_user
from ..schemas.query_schema import QueryRequest, QueryResponse
from ..models.query_model import Query
from ..rag.pipeline import RAGPipeline


router = APIRouter(prefix="/query", tags=["RAG Query"])

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
    """Effectue une requête RAG"""
    try:
        start_time = time.time()
        
        pipeline = get_rag_pipeline()
        answer = pipeline.query(request.question)
        
        latency_ms = (time.time() - start_time) * 1000
        
        new_query = Query(
            user_id=current_user_id,
            question=request.question,
            answer=answer,
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
            detail=f"Erreur: {str(e)}"
        )
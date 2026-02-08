"""RAG query endpoints"""
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

# Singleton pipeline instance
rag_pipeline = RAGPipeline()


@router.post("/", response_model=QueryResponse)
def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Execute a RAG query.
    
    Retrieves relevant documents and generates an answer
    using the LLM with retrieved context.
    
    Args:
        request: Question to answer
        db: Database session
        current_user_id: Authenticated user ID
        
    Returns:
        Query response with answer and metadata
    """
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty"
        )
    
    start_time = time.time()
    
    # Execute RAG pipeline
    answer, cluster_id = rag_pipeline.query(request.question)
    
    # Calculate latency
    latency_ms = (time.time() - start_time) * 1000
    
    # Save to database
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
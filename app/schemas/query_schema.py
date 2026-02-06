from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Requête utilisateur"""
    question: str = "Comment réinitialiser un mot de passe Windows?"


class QueryResponse(BaseModel):
    """Réponse API"""
    id: int
    user_id: int
    question: str
    answer: str
    cluster: Optional[int] = None
    latency_ms: float
    created_at: datetime
    
    class Config:
        from_attributes = True
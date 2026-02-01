"""
Schemas Pydantic pour les queries (questions/réponses)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class QueryCreate(BaseModel):
    """Schema pour créer une query"""
    question: str


class QueryResponse(BaseModel):
    """Schema pour retourner une query"""
    id: int
    user_id: int
    question: str
    answer: str
    cluster: Optional[int] = None
    latency_ms: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class QueryRequest(BaseModel):
    """Schema pour la requête API"""
    question: str
    n_results: int = 3  # Nombre de chunks à récupérer
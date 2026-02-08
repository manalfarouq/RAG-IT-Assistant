from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_serializer


class QueryRequest(BaseModel):
    """Requête utilisateur"""
    question: str = Field(..., example="Quels sont les fondamentaux du support IT ?")


class QueryResponse(BaseModel):
    """Réponse API"""
    id: int
    user_id: int
    question: str
    answer: str
    cluster: Optional[str] = None 
    latency_ms: float
    created_at: datetime
    
    @field_serializer('latency_ms')
    def format_latency(self, value: float) -> str:
        total_seconds = value / 1000
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        
        if minutes > 0:
            return f"{minutes}m {seconds:.2f}s"
        else:
            return f"{seconds:.2f}s"
    
    @field_serializer('created_at')
    def format_datetime(self, value: datetime) -> str:
        return value.strftime("%d/%m/%Y %H:%M:%S")
    
    class Config:
        from_attributes = True
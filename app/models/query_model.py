"""Query database model"""
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.database import Base


class Query(Base):
    """
    Stores user queries and RAG responses.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        question: User's question
        answer: RAG-generated answer
        cluster: Assigned category/cluster
        latency_ms: Response time in milliseconds
        created_at: Timestamp
    """
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    cluster = Column(String, nullable=True)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="queries")
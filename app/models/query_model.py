"""
Modèles SQLAlchemy pour PostgreSQL
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base

class Query(Base):
    """Table des questions/réponses"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    cluster = Column(Integer, nullable=True)  # Pour le clustering ML
    latency_ms = Column(Float, nullable=True)  # Temps de réponse
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation : une query appartient à un utilisateur
    user = relationship("User", back_populates="queries")
    
    def __repr__(self):
        return f"<Query(id={self.id}, question={self.question[:50]}...)>"
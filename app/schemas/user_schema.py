"""
Schemas Pydantic pour les utilisateurs
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Schema de base pour un utilisateur"""
    email: EmailStr


class UserCreate(UserBase):
    """Schema pour créer un utilisateur"""
    password: str


class UserResponse(UserBase):
    """Schema pour retourner un utilisateur (sans mot de passe)"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Pour SQLAlchemy models



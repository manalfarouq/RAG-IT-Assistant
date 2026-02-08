"""
Schemas pour l'authentification et les utilisateurs
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Authentication
class LoginRequest(BaseModel):
    """Login"""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Inscription"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Réponse token"""
    access_token: str
    token_type: str = "bearer"


# User
class UserResponse(BaseModel):
    """Réponse utilisateur"""
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
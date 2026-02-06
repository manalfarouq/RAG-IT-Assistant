"""
Schemas pour l'authentification
"""
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema pour le login"""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Schema pour l'inscription"""
    email: EmailStr
    password: str
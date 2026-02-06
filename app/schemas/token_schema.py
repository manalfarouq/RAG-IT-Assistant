"""
Schemas pour les tokens JWT
"""
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema de réponse après login"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données contenues dans le token"""
    email: Optional[str] = None
    user_id: Optional[int] = None
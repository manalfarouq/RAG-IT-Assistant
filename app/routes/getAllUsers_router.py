"""
Route pour récupérer les utilisateurs
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Récupère tous les utilisateurs
    (Sans les mots de passe)
    """
    users = db.query(User).all()
    return users
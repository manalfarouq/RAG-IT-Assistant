"""
Route d'inscription
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..auth.token_auth import create_user, get_user_by_email
from ..schemas.login_request_schema import RegisterRequest
from ..schemas.user_schema import UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur
    
    - Vérifie que l'email n'existe pas déjà
    - Hashe le mot de passe
    - Crée l'utilisateur dans la DB
    """
    # Vérifier si l'utilisateur existe déjà
    existing_user = get_user_by_email(db, request.email)
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    # Créer le nouvel utilisateur
    user = create_user(db, email=request.email, password=request.password)
    
    return user
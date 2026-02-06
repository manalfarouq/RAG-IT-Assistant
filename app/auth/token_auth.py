from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional

from ..core.config import settings
from ..schemas.token_schema import TokenData, Token
from ..models.user_model import User


security = HTTPBearer()

# Configuration du contexte de hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en clair correspond au hash
    
    Args:
        plain_password: Mot de passe en clair
        hashed_password: Mot de passe hashé
    
    Returns:
        True si le mot de passe correspond, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash un mot de passe
    
    Args:
        password: Mot de passe en clair
    
    Returns:
        Mot de passe hashé
    """
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Récupère un utilisateur par son email
    
    Args:
        db: Session de base de données
        email: Email de l'utilisateur
    
    Returns:
        L'utilisateur si trouvé, None sinon
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str) -> User:
    """
    Crée un nouvel utilisateur
    
    Args:
        db: Session de base de données
        email: Email de l'utilisateur
        password: Mot de passe en clair
    
    Returns:
        L'utilisateur créé
    """
    hashed_password = get_password_hash(password)
    
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authentifie un utilisateur par email et mot de passe
    
    Args:
        db: Session de base de données
        email: Email de l'utilisateur
        password: Mot de passe en clair
    
    Returns:
        L'utilisateur si l'authentification réussit, None sinon
    """
    user = get_user_by_email(db, email)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Créer un token JWT
    
    Args:
        data: Données à encoder dans le token
        expires_delta: Durée de validité du token (optionnel)
    
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_token(user_id: int) -> str:
    """
    Créer un token JWT (ancienne fonction, gardée pour rétrocompatibilité)
    
    Args:
        user_id: ID de l'utilisateur
    
    Returns:
        Token JWT encodé
    """
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> TokenData:
    """
    Vérifier et décoder un token JWT
    
    Args:
        token: Token JWT à vérifier
    
    Returns:
        TokenData avec les informations de l'utilisateur
    
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token invalide"
            )
        
        return TokenData(user_id=user_id, username=username)
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expiré"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Dépendance FastAPI pour récupérer l'utilisateur actuel depuis le token JWT
    
    Args:
        credentials: Credentials HTTP Bearer
    
    Returns:
        user_id de l'utilisateur authentifié
    
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    token = credentials.credentials
    token_data = verify_token(token)
    return token_data.user_id
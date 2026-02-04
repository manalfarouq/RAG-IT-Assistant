"""
Configuration de la connexion PostgreSQL avec SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Créer le moteur de connexion à PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Vérifier la connexion avant utilisation
    pool_size=10,        # Nombre de connexions dans le pool
    max_overflow=20,     # Connexions supplémentaires si nécessaire
    echo=False           # Mettre True pour voir les requêtes SQL (debug)
)

# Créer une fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour tous les modèles SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Dependency pour FastAPI
    Crée une session DB et la ferme automatiquement après usage

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

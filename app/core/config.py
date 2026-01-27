# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "RAG IT Assistant"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # RAG Configuration
    PDF_PATH: str = "data/raw/data.pdf"
    CHROMA_PERSIST_DIR: str = "data/vector_db/chroma"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # LLM Configuration
    LLM_PROVIDER: str = "huggingface"
    LLM_MODEL: str = "google/flan-t5-base"
    LLM_TEMPERATURE: float = 0.3
    LLM_TOP_K: int = 3
    
    # API Keys (optionnelles)
    HUGGINGFACE_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
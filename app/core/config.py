"""Application configuration settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    
    All sensitive values should be stored in .env file.
    """
    
    # API Configuration
    PROJECT_NAME: str = "RAG IT Assistant"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # RAG Configuration
    PDF_PATH: str = "/app/data/raw/data.pdf"
    CHROMA_PERSIST_DIR: str = "/tmp/chroma"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 50
    
    # LLM Configuration  
    LLM_MODEL: str = "gemini-2.5-flash"
    
    # API Keys
    HF_TOKEN: Optional[str] = None
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
"""Routes d'administration"""
from fastapi import APIRouter, HTTPException
from app.scripts.init_vector_store import main as init_vector_store
import logging

router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)

@router.post("/reindex")
def reindex_vector_store():
    """Réindexe le vector store (nécessite redémarrage de l'app après)"""
    try:
        logger.info("🔄 Réindexation du vector store...")
        init_vector_store()
        return {
            "status": "success",
            "message": "Vector store réindexé. Redémarrez l'application pour appliquer les changements."
        }
    except Exception as e:
        logger.error(f"❌ Erreur lors de la réindexation : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def admin_health():
    """Sanity check"""
    return {"status": "ok", "service": "admin"}
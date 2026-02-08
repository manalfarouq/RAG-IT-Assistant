"""
Route pour les requêtes RAG (Version améliorée)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import time
import logging

from ..db.database import get_db
from ..auth.token_auth import get_current_user
from ..schemas.query_schema import QueryRequest, QueryResponse
from ..models.query_model import Query
from ..rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["RAG Query"])

rag_pipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """
    Retourne l'instance du pipeline RAG (singleton) avec initialisation lazy
    """
    global rag_pipeline
    if rag_pipeline is None:
        try:
            logger.info("Initialisation du pipeline RAG...")
            rag_pipeline = RAGPipeline()
            logger.info("Pipeline RAG initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur fatale lors de l'initialisation du pipeline: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Le service RAG n'est pas disponible. Veuillez réessayer plus tard."
            )
    return rag_pipeline


@router.post("/", response_model=QueryResponse)
def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Effectue une requête RAG avec gestion complète des erreurs
    
    Args:
        request: La requête contenant la question
        db: Session de base de données
        current_user_id: ID de l'utilisateur authentifié
        
    Returns:
        QueryResponse: La réponse avec métadonnées
        
    Raises:
        HTTPException: En cas d'erreur
    """
    start_time = time.time()
    query_id = None
    
    try:
        # Validation de la requête
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La question ne peut pas être vide"
            )
        
        logger.info(f"Nouvelle requête de l'utilisateur {current_user_id}: {request.question[:100]}...")
        
        # Obtention du pipeline
        try:
            pipeline = get_rag_pipeline()
        except Exception as e:
            logger.error(f"Impossible d'obtenir le pipeline RAG: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Le service RAG n'est pas disponible"
            )
        
        # Exécution de la requête RAG
        try:
            answer, cluster_id = pipeline.query(request.question)
        except Exception as e:
            logger.error(f"Erreur lors du traitement RAG: {e}", exc_info=True)
            # Réponse de fallback
            answer = (
                "Désolé, une erreur s'est produite lors du traitement de votre question. "
                "Veuillez réessayer ou reformuler votre question."
            )
            cluster_id = "Erreur"
        
        # Calcul de la latence
        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"Requête traitée en {latency_ms:.2f}ms")
        
        # Sauvegarde dans la base de données
        try:
            new_query = Query(
                user_id=current_user_id,
                question=request.question.strip(),
                answer=answer,
                cluster=cluster_id,
                latency_ms=round(latency_ms, 2),
                created_at=datetime.now(timezone.utc)
            )
            
            db.add(new_query)
            db.commit()
            db.refresh(new_query)
            
            query_id = new_query.id
            logger.info(f"Requête sauvegardée avec l'ID {query_id}")
            
            return new_query
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur base de données lors de la sauvegarde: {e}")
            db.rollback()
            
            # On retourne quand même la réponse même si la sauvegarde a échoué
            # mais on log l'erreur
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="La réponse a été générée mais n'a pas pu être sauvegardée"
            )
    
    except HTTPException:
        # Re-raise les HTTPException sans modification
        raise
    
    except Exception as e:
        logger.error(f"Erreur inattendue dans query_rag: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )
    
    finally:
        # Log final avec durée totale
        total_time = (time.time() - start_time) * 1000
        logger.info(
            f"Requête terminée en {total_time:.2f}ms "
            f"(user_id={current_user_id}, query_id={query_id})"
        )


@router.get("/health")
def health_check():
    """
    Endpoint de santé pour vérifier que le service RAG est opérationnel
    """
    try:
        pipeline = get_rag_pipeline()
        return {
            "status": "healthy",
            "service": "RAG Query",
            "pipeline_initialized": pipeline is not None
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )
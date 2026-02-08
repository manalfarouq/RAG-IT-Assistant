"""
Vector store avec ChromaDB
"""
from pathlib import Path
import logging

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_core.documents import Document

from ..core.config import settings
from ..services.embeddings import embed_text, embed_texts

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self.persist_dir = Path(settings.CHROMA_PERSIST_DIR)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name="it_support_docs"
        )
        
        logger.info(f"📊 Collection chargée avec {self.collection.count()} documents")

    def add_documents(self, documents):
        # Récupérer le nombre actuel de documents pour générer des IDs uniques
        current_count = self.collection.count()
        logger.info(f"📊 Documents actuels dans la collection : {current_count}")
        
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [f"doc_{current_count + i}" for i in range(len(documents))]

        embeddings = embed_texts(texts)

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        # Vérifier que l'ajout a fonctionné
        new_count = self.collection.count()
        logger.info(f"✅ Documents après ajout : {new_count} (ajoutés : {new_count - current_count})")

    def search(self, query, n_results=3):
        logger.info(f"🔍 Searching for: {query}")
        logger.info(f"📊 Collection size: {self.collection.count()}")
        
        query_embedding = embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        logger.info(f"📦 Found {len(results['ids'][0])} results")
        
        if results['ids'][0]:
            logger.info(f"📏 Best distance: {results['distances'][0][0]:.3f}")

        return [
            {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
            for i in range(len(results["ids"][0]))
        ]
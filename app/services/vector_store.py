"""
Vector store avec ChromaDB
"""
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_core.documents import Document

from app.core.config import settings
from app.services.embeddings import embed_text, embed_texts


class VectorStore:
    def __init__(self):
        self.persist_dir = Path(settings.CHROMA_PERSIST_DIR)
        self.persist_dir.mkdir(parents=True, exist_ok=True) # Créer le dossier où Chroma va stocker les données

        self.client = chromadb.PersistentClient( # crées une connexion persistante à ChromaDB.
            path=str(self.persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection( # crées une collection (comme une table) pour stocker les embeddings.
            name="it_support_docs"
        )

    def add_documents(self, documents):
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]

        embeddings = embed_texts(texts)

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query, n_results=3):
        query_embedding = embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return [
            {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
            for i in range(len(results["ids"][0]))
        ]

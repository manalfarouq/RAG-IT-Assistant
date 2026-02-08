"""Chargement et découpage d'un PDF"""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

def load_and_split_pdf(pdf_path=None) -> List[Document]:
    """Charge et découpe un PDF en chunks"""
    
    path = Path(pdf_path or settings.PDF_PATH)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    logger.info(f"📄 Loading PDF: {path}")
    
    documents = PyPDFLoader(str(path)).load()
    logger.info(f"📖 {len(documents)} pages loaded")
    
    # Enrichir métadonnées
    for i, doc in enumerate(documents):
        page_num = i + 1
        doc.metadata['page_number'] = page_num
        doc.metadata['source'] = 'PDF'
        
        # Détecter chapitre
        content_lower = doc.page_content.lower()
        if 'chapter' in content_lower:
            lines = doc.page_content.split('\n')
            for line in lines:
                if 'chapter' in line.lower() and len(line) < 100:
                    doc.metadata['chapter'] = line.strip()
                    break

    # CHUNKS PLUS PETITS pour meilleure précision
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,      # ← Réduit de 500 à 300
        chunk_overlap=50,    # ← Réduit de 100 à 50
        length_function=len,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    )

    chunks = splitter.split_documents(documents)
    logger.info(f"✂️ {len(chunks)} chunks created")
    
    if chunks:
        logger.info(f"📝 Sample chunk:\n{chunks[0].page_content[:150]}...")
    
    return chunks
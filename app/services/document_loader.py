"""PDF document loading and processing"""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)


def load_and_split_pdf(pdf_path: str = None) -> List[Document]:
    """
    Load PDF and split into chunks.
    
    Args:
        pdf_path: Path to PDF file (uses settings.PDF_PATH if None)
        
    Returns:
        List of Document chunks with metadata
        
    Raises:
        FileNotFoundError: If PDF doesn't exist
    """
    path = Path(pdf_path or settings.PDF_PATH)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    logger.info(f"Loading PDF: {path}")
    
    # Load PDF pages
    documents = PyPDFLoader(str(path)).load()
    logger.info(f"Loaded {len(documents)} pages")
    
    # Enrich metadata
    for i, doc in enumerate(documents):
        page_num = i + 1
        doc.metadata['page_number'] = page_num
        doc.metadata['source'] = 'PDF'
        
        # Detect chapter information
        content_lower = doc.page_content.lower()
        if 'chapter' in content_lower:
            lines = doc.page_content.split('\n')
            for line in lines:
                if 'chapter' in line.lower() and len(line) < 100:
                    doc.metadata['chapter'] = line.strip()
                    break

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    )

    chunks = splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    
    if chunks:
        logger.info(f"Sample chunk: {chunks[0].page_content[:150]}...")
    
    return chunks
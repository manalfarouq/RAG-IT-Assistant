"""
Chargement et découpage d'un PDF
"""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..core.config import settings


def load_and_split_pdf(pdf_path=None):
    path = Path(pdf_path or settings.PDF_PATH)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    documents = PyPDFLoader(path).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )

    return splitter.split_documents(documents)


# if __name__ == "__main__":
#     chunks = load_and_split_pdf()
#     print(f"Chunks créés : {len(chunks)}")
#     print(chunks[0].page_content[:200])

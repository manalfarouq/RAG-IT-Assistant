"""
Chargement des documents PDF
"""
from app.core.config import settings

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

document = PdfFileReader(open(settings.PDF_PATH, 'rb'))

metadata = document.getDocumentInfo()
print (metadata)
















# from langchain_community.document_loaders import PyPDFLoader
# from typing import List
# from langchain_core.documents import Document 
# from app.core.config import settings
# from app.core.logging import logger


# class DocumentLoader:
#     """Classe pour charger les documents PDF"""
    
#     def __init__(self, pdf_path: str = None):
#         self.pdf_path = pdf_path or settings.PDF_PATH
#         logger.info(f"DocumentLoader initialized with path: {self.pdf_path}")
    
#     def load(self) -> List[Document]:
#         """
#         Charge le PDF et retourne la liste des documents
        
#         Returns:
#             List[Document]: Liste des documents (1 par page)
#         """
#         try:
#             logger.info(f"Loading PDF from: {self.pdf_path}")
#             loader = PyPDFLoader(self.pdf_path)
#             documents = loader.load()
            
#             logger.info(f"Loaded {len(documents)} pages from PDF")
            
#             # Ajouter des métadonnées supplémentaires
#             for i, doc in enumerate(documents):
#                 doc.metadata["source"] = self.pdf_path
#                 doc.metadata["page_number"] = i + 1
            
#             return documents
            
#         except FileNotFoundError:
#             logger.error(f"PDF file not found: {self.pdf_path}")
#             raise
#         except Exception as e:
#             logger.error(f"Error loading PDF: {str(e)}")
#             raise


# def load_pdf(pdf_path: str = None) -> List[Document]:
#     """
#     Fonction utilitaire pour charger un PDF
    
#     Args:
#         pdf_path: Chemin vers le PDF (optionnel)
    
#     Returns:
#         List[Document]: Liste des documents
#     """
#     loader = DocumentLoader(pdf_path)
#     return loader.load()

"""
Initialisation du Vector Store avec vos questions et PDF
"""
from app.services.vector_store import VectorStore
from app.scripts.questions import questions_data  # <-- ton fichier questions.py
from app.services.document_loader import load_and_split_pdf

class DummyDoc:
    """Classe pour transformer une question en objet document compatible VectorStore"""
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata or {}

def main():
    print("🔧 Initialisation du Vector Store...")

    vector_store = VectorStore()

    documents_to_index = []

    # 1️⃣ Ajouter les questions
    for q in questions_data:
        documents_to_index.append(DummyDoc(q["question"], {"category": q["category"]}))

    # 2️⃣ Ajouter les documents PDF
    try:
        pdf_chunks = load_and_split_pdf()
        documents_to_index.extend(pdf_chunks)
    except FileNotFoundError as e:
        print(f"⚠️ {e}")

    if not documents_to_index:
        print("❌ Aucun document à indexer.")
        return

    # 3️⃣ Indexer
    vector_store.add_documents(documents_to_index)

    print(f"✅ {len(documents_to_index)} documents indexés avec succès.")


if __name__ == "__main__":
    main()

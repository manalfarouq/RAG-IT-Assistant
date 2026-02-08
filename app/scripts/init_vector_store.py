"""
Initialisation du Vector Store avec vos questions et PDF
"""
from app.services.vector_store import VectorStore
from app.scripts.questions import questions_data
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
    print(f"📋 Ajout de {len(questions_data)} questions...")
    for q in questions_data:
        documents_to_index.append(DummyDoc(
            q["question"], 
            {"category": q["category"], "source": "predefined"}
        ))

    # 2️⃣ Ajouter les documents PDF
    print("📚 Chargement du PDF...")
    try:
        pdf_chunks = load_and_split_pdf()
        documents_to_index.extend(pdf_chunks)
        print(f"✅ {len(pdf_chunks)} chunks de PDF ajoutés")
    except FileNotFoundError as e:
        print(f"⚠️ {e}")

    if not documents_to_index:
        print("❌ Aucun document à indexer.")
        return

    # 3️⃣ Indexer
    print(f"💾 Indexation de {len(documents_to_index)} documents...")
    vector_store.add_documents(documents_to_index)

    print(f"✅ {len(documents_to_index)} documents indexés avec succès.")
    
    # 4️⃣ Test rapide
    print("\n🔍 Test de recherche...")
    test_results = vector_store.search("imprimante réseau", n_results=2)
    for i, r in enumerate(test_results, 1):
        print(f"  {i}. [Distance: {r['distance']:.3f}] {r['document'][:80]}...")


if __name__ == "__main__":
    main()
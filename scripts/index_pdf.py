"""
Indexation du PDF dans ChromaDB
"""
from app.services.document_loader import load_and_split_pdf
from app.services.vector_store import VectorStore

print("🔄 Chargement et découpage du PDF...")
chunks = load_and_split_pdf()
print(f"✅ {len(chunks)} chunks créés")

print("\n🔄 Indexation dans ChromaDB...")
store = VectorStore()
store.add_documents(chunks)

print(f"\n✅ Indexation terminée!")
print(f"Total documents: {store.collection.count()}")

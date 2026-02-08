"""Vector store initialization script"""
from app.services.vector_store import VectorStore
from app.scripts.questions import questions_data
from app.services.document_loader import load_and_split_pdf


class DummyDoc:
    """Simple document wrapper for questions"""
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata or {}


def main():
    """Initialize vector store with questions and PDF chunks"""
    print("Initializing vector store...")

    vector_store = VectorStore()
    documents_to_index = []

    # Add predefined questions
    print(f"Adding {len(questions_data)} questions...")
    for q in questions_data:
        documents_to_index.append(DummyDoc(
            q["question"], 
            {"category": q["category"], "source": "predefined"}
        ))

    # Add PDF chunks
    print("Loading PDF...")
    try:
        pdf_chunks = load_and_split_pdf()
        documents_to_index.extend(pdf_chunks)
        print(f"Added {len(pdf_chunks)} PDF chunks")
    except FileNotFoundError as e:
        print(f"Warning: {e}")
        print("Indexing questions only")

    if not documents_to_index:
        print("Error: No documents to index")
        return

    # Index documents
    print(f"Indexing {len(documents_to_index)} documents...")
    vector_store.add_documents(documents_to_index)

    print(f"Successfully indexed {len(documents_to_index)} documents")
    
    # Quick test
    print("\nRunning search test...")
    test_results = vector_store.search("network troubleshooting", n_results=2)
    for i, r in enumerate(test_results, 1):
        print(f"  {i}. [Distance: {r['distance']:.3f}] {r['document'][:80]}...")


# if __name__ == "__main__":
#     main()
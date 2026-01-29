"""
Test du pipeline RAG complet
"""
from app.rag.pipeline import RAGPipeline

# Questions de test
questions = [
    "Comment réinitialiser un mot de passe Windows?",
    "Quelle est la procédure de sauvegarde?"
]

print("\n" + "="*80)
print("TEST DU PIPELINE RAG")
print("="*80)

rag = RAGPipeline()

for i, question in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"Question {i}: {question}")
    print("="*80)
    
    result = rag.query(question)
    
    print(f"\nRéponse:")
    print(result["answer"])
    
    print(f"\nChunks utilisés: {result['n_chunks_used']}")
    for j, chunk in enumerate(result["context_chunks"], 1):
        print(f"   Chunk {j} (distance: {chunk['distance']:.4f})")

print("\nTest terminé!")
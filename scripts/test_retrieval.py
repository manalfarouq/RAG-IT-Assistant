"""
Test de recherche sémantique sur 5 questions
"""
from app.services.vector_store import VectorStore
import logging

logging.basicConfig(level=logging.INFO)

# 5 questions de test IT
test_questions = [
    "Comment réinitialiser un mot de passe Windows?",
    "Quelle est la procédure de sauvegarde des données?",
    "Comment installer un nouveau logiciel?",
    "Que faire en cas de panne réseau?",
    "Comment configurer une imprimante?"
]

print("\n" + "="*80)
print("TEST DE RECHERCHE SÉMANTIQUE")
print("="*80)

store = VectorStore()

for i, question in enumerate(test_questions, 1):
    print(f"\n\n{'='*80}")
    print(f"Question {i}: {question}")
    print("="*80)
    
    results = store.search(question, n_results=3)
    
    for j, result in enumerate(results, 1):
        print(f"\nRésultat {j} (distance: {result['distance']:.4f}):")
        print(f"   {result['document'][:200]}...")
        if 'page' in result['metadata']:
            print(f"   Page: {result['metadata']['page']}")

print("\n\nTest terminé!")

# RAG IT Assistant

Assistant intelligent de support IT basé sur le livre **"The IT Support Handbook"** par Mike Halsey, utilisant la technologie RAG (Retrieval-Augmented Generation).

## Description

Ce projet est un système de questions-réponses intelligent qui combine :
- **RAG (Retrieval-Augmented Generation)** pour des réponses contextuelles précises
- **108 questions pré-indexées** couvrant tous les chapitres du livre
- **770 chunks PDF** extraits du manuel IT Support
- **Clustering automatique** des questions par catégorie
- **API REST** avec FastAPI
- **Base de données PostgreSQL** pour l'historique

## Installation Rapide

### Prérequis
- Docker & Docker Compose
- Python 3.11+

### Démarrage
```bash
# 1. Cloner le projet
git clone <votre-repo>
cd RAG-IT-Assistant

# 2. Créer le fichier .env
cp .env.example .env
# Ajouter votre clé API Gemini dans .env

# 3. Lancer avec Docker
docker-compose up -d

# 4. Initialiser la base vectorielle
docker exec -it rag-it-assistant-app-1 python -m app.scripts.init_vector_store

# 5. Accéder à l'API
# http://localhost:8000/docs
```

## Utilisation

### Créer un compte
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Se connecter
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password123"}'
```

### Poser une question
```bash
curl -X POST http://localhost:8000/query/ \
  -H "Authorization: Bearer <votre-token>" \
  -H "Content-Type: application/json" \
  -d '{"question":"Comment résoudre un problème réseau ?"}'
```

## Structure du Projet
```
RAG-IT-Assistant/
├── app/
│   ├── rag/              # Pipeline RAG
│   ├── services/         # Services (LLM, embeddings, clustering)
│   ├── routes/           # Endpoints API
│   ├── models/           # Modèles de données
│   └── scripts/          # Scripts d'initialisation
├── data/
│   ├── raw/              # PDF source
│   └── vector_db/        # Base vectorielle ChromaDB
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Technologies

| Technologie | Usage |
|------------|-------|
| **FastAPI** | API REST |
| **PostgreSQL** | Base de données |
| **ChromaDB** | Base vectorielle |
| **Sentence Transformers** | Embeddings (bge-small-en-v1.5) |
| **Google Gemini** | Génération de réponses |
| **scikit-learn** | Clustering K-Means |
| **LangChain** | Traitement PDF et texte |

## Données

- **108 questions** pré-indexées organisées par catégorie
- **770 chunks** extraits du PDF "The IT Support Handbook"
- **12 catégories** de clustering automatique

### Catégories principales
- Fondamentaux IT
- Dépannage & Méthodologie
- Systèmes & Architecture
- Documentation
- Outils Windows
- Support à distance

## 🔧 Configuration

Fichier `.env` requis :
```env
GEMINI_API_KEY=votre_clé_ici
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=rag_db
DATABASE_URL=postgresql://user:password@db:5432/rag_db
```

## Exemple de Réponse
```json
{
  "id": 1,
  "user_id": 1,
  "question": "Comment diagnostiquer un problème réseau ?",
  "answer": "Selon le livre, page 38, commencez par un processus d'élimination...",
  "cluster": "Dépannage & Méthodologie",
  "latency_ms": "2.45s",
  "created_at": "08/02/2026 17:24:19"
}
```

## Tests
```bash
# Tester la recherche vectorielle
docker exec -it rag-it-assistant-app-1 python -c "
from app.services.vector_store import VectorStore
vs = VectorStore()
results = vs.search('troubleshooting network', n_results=3)
for r in results: print(r['document'][:100])
"
```

## Ressources

- **Livre source** : "The IT Support Handbook" - Mike Halsey (Apress, 2019)
- **Modèle d'embeddings** : BAAI/bge-small-en-v1.5
- **LLM** : Google Gemini 1.5 Flash

## 🤝 Contribution

Ce projet est à but éducatif. Contributions bienvenues !


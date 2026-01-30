-- Créer l'utilisateur
CREATE USER raguser WITH PASSWORD 'ragpassword';

-- Créer la base de données
CREATE DATABASE rag_db OWNER raguser;

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE rag_db TO raguser;

-- Créer la base de données si elle n'existe pas
SELECT 'CREATE DATABASE rag_db OWNER raguser'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'rag_db')\gexec

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE rag_db TO raguser;

-- Se connecter à rag_db pour créer les tables
\c rag_db

-- Créer les tables
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    cluster INTEGER,
    latency_ms FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Créer les index pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_queries_user_id ON queries(user_id);
CREATE INDEX IF NOT EXISTS idx_queries_created_at ON queries(created_at);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Donner les permissions sur les tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO raguser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO raguser;
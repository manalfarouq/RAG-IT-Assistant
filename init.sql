-- Créer l'utilisateur
CREATE USER raguser WITH PASSWORD 'ragpassword';

-- Créer la base de données
CREATE DATABASE rag_db OWNER raguser;

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE rag_db TO raguser;


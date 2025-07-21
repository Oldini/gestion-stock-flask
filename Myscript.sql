-- Création de la table utilisateur
CREATE TABLE IF NOT EXISTS utilisateur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Création de la table produit
CREATE TABLE IF NOT EXISTS produit (
    id SERIAL PRIMARY KEY,
    nom VARCHAR NOT NULL,
    prix FLOAT NOT NULL,
    utilisateur_id INTEGER REFERENCES utilisateur(id)
);

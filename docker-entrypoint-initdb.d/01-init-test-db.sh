#!/bin/bash
set -e

# Création de la base de données de test
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE stock_test;
    GRANT ALL PRIVILEGES ON DATABASE stock_test TO $POSTGRES_USER;
EOSQL

# Vous pouvez ajouter d'autres commandes d'initialisation ici si nécessaire

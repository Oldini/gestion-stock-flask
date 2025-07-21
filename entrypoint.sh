#!/bin/bash

echo "⏳ Attente de PostgreSQL..."

# "db" = nom du service PostgreSQL défini dans docker-compose.yml
# "5432" = port par défaut de PostgreSQL
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL est prêt. Lancement de Flask..."

# Active ton environnement si nécessaire
# source venv/bin/activate  ← si tu utilises un venv

# Lance ton app Flask
python run.py

#!/bin/bash

echo "⏳ Attente de PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL est prêt. Initialisation des migrations..."

# 📁 Créer le dossier migrations s'il n'existe pas (uniquement la 1re fois)
if [ ! -d "migrations" ]; then
    flask db init
fi

flask db migrate -m "Initial migration"
flask db upgrade

echo "🚀 Lancement de l'application Flask..."
exec flask run

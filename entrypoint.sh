#!/bin/bash

echo "⏳ Attente de PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL est prêt."

# Initialiser la migration si nécessaire
if [ ! -d "migrations" ]; then
  echo "📁 Initialisation de flask-migrate..."
  flask db init
fi

# Appliquer les migrations
echo "⬆️ Mise à jour de la base de données..."
flask db migrate -m "Auto migration"
flask db upgrade

# Lancer l'application Flask
echo "🚀 Lancement de Flask"
exec flask run --host=0.0.0.0 --port=5000

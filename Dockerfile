# ✅ Étape 1: Choisir une image Python légère
FROM python:3.11-slim

# ✅ Étape 2: Créer un répertoire de travail
WORKDIR /app

# ✅ Étape 3: Copier le fichier des dépendances
COPY requirements.txt .

# ✅ Étape 4: Créer un environnement virtuel
RUN python -m venv venv

# ✅ Étape 5: Activer le venv dans le conteneur
ENV PATH="/app/venv/bin:$PATH"

# ✅ Étape 6: Installer les dépendances dans le venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# ✅ Étape 7: Copier tout le reste du projet
COPY . .

# ✅ Étape 8: Exposer le port sur lequel Flask écoute
EXPOSE 5000

# ✅ Étape 9: Lancer l'application
CMD ["python", "run.py"]


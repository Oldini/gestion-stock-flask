 Étape 1: Choisir l'image de base (Python 3.11)
FROM python:3.11-slim

# Étape 2: Définir un répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3: Copier le fichier des dépendances
COPY requirements.txt /app/requirements.txt

# Étape 4: Créer l'environnement virtuel et l'activer
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Étape 5: Installer les dépendances dans l'environnement virtuel
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6: Copier le reste du projet dans le conteneur
COPY . /app

# Étape 7: Exposer le port de l'application
EXPOSE 5000

# Étape 8: Définir la commande pour lancer l'application
CMD ["python", "run.py"]


# ✅ Étape 1: Image Python légère
FROM python:3.11-slim

# ✅ Étape 2: Définir le répertoire de travail
WORKDIR /app

# ✅ Étape 3: Copier les dépendances
COPY requirements.txt .

# ✅ Étape 4: Installer les dépendances avec vérification
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip list

# ✅ Étape 5: Copier tout le projet
COPY . .

# ✅ Étape 6: Copier et rendre executable le script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


# ✅ Étape 7: Configuration Flask pour production
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# ✅ Étape 8: Exposer le port Flask
EXPOSE 5000

# ✅ Étape 9: Lancer l'application Flask
ENTRYPOINT ["/entrypoint.sh"]


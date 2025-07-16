import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration de base, utilisée en développement ou en production."""
    
    # Clé secrète pour sécuriser les sessions Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change')

    # URI de la base de données principale (PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Désactive le suivi des modifications (plus performant)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration du serveur
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # Configuration des logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

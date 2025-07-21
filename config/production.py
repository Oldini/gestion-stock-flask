from config.base import Config
import os

class ProductionConfig(Config):
    """Configuration spécifique à la production."""

    # On peut forcer l'URL de production ici (optionnel si géré par .env)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


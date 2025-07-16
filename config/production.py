from config.base import Config

class ProductionConfig(Config):
    """Configuration spécifique à la production."""

    # On peut forcer l'URL de production ici (optionnel si géré par .env)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:oldini031001@localhost:5432/Stock'

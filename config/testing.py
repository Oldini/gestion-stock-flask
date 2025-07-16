from config.base import Config
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class TestingConfig(Config):
    """Configuration spéciale pour les tests unitaires."""

    TESTING = True  # Active le mode test dans Flask
    WTF_CSRF_ENABLED = False  # Désactive la protection CSRF pour les formulaires
    PRESERVE_CONTEXT_ON_EXCEPTION = False  # Ne garde pas le contexte après les exceptions

    # Base de données de test (PostgreSQL ou SQLite fallback)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'test.db')
    )

    # Logs spécifiques pour les tests
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'test.log'

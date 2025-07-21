import pytest
from dotenv import load_dotenv
from app import create_app, db
from app.models import Utilisateur
import os

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-test-key')


@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all() # Création de la base de test
        yield app


        
        # Nettoyage complet
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_db(app):
    """Fixture pour peupler la base de test"""
    with app.app_context():
        # Ajoutez ici des données de test si nécessaire
        test_user = Utilisateur(nom="testuser", password="hashed_pw")
        db.session.add(test_user)
        db.session.commit()
        yield
        db.session.rollback()

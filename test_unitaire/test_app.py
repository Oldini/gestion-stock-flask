import pytest
from app import create_app, db
from config.testing import TestingConfig
from werkzeug.security import generate_password_hash
from app.models import Utilisateur

@pytest.fixture
def app():
    """Crée l'application Flask avec la config de test"""
    app = create_app(TestingConfig)
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Crée un client de test à partir de l'app"""
    return app.test_client()

def test_accueil(client):
    """Test de la route d'accueil"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Bienvenue" in response.data
    assert b"Connexion" in response.data
    assert b"Cr\xc3\xa9er un compte" in response.data  # Utiliser la séquence d'échappement UTF-8

def test_dashboard_access(client):
    """Test l'accès au dashboard sans être connecté"""
    response = client.get('/dashboard')
    assert response.status_code == 200  # La route est accessible sans authentification
    assert b"Tableau de bord" in response.data

def test_dashboard_access_auth(client, app):
    """Test l'accès au dashboard avec authentification"""
    with app.app_context():
        # Crée un utilisateur de test
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw, role='utilisateur')
        db.session.add(user)
        db.session.commit()

        # Se connecter
        client.post('/auth/login', data={'nom': 'testuser', 'password': 'testpass123'}, follow_redirects=True)

        # Accéder au dashboard
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b"Tableau de bord" in response.data
        assert b"D\xc3\xa9connexion" in response.data  # Utiliser la séquence d'échappement UTF-8

def test_test_db(client):
    """Test la route de test de la base de données"""
    response = client.get('/test_db')
    assert response.status_code == 200
    assert b"La connexion \xc3\xa0 la base de donn\xc3\xa9es fonctionne !" in response.data  # Utiliser les séquences d'échappement UTF-8

import pytest
from flask import session
from app import create_app
from app.models import db, Utilisateur
from werkzeug.security import generate_password_hash
from config.testing import TestingConfig


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


def test_login_page_get(client):
    """Test l'accès à la page de login (GET)"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Connexion' in response.data


def test_login_success(client, app):
    """Test une connexion valide"""
    with app.app_context():
        # Crée un utilisateur de test avec un rôle
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw, role='utilisateur')
        db.session.add(user)
        db.session.commit()

        # Tente de se connecter
        response = client.post('/auth/login', 
                             data={'nom': 'testuser', 'password': 'testpass123'},
                             follow_redirects=True)
        
        assert response.status_code == 200
        # Vérifie que nous sommes sur la page dashboard
        assert 'Tableau de bord'.encode() in response.data
        
        # Vérifie la session
        with client.session_transaction() as sess:
            assert sess['user_id'] == user.id
            assert sess['user_nom'] == 'testuser'
            assert sess['user_role'] == 'utilisateur'


def test_login_missing_fields(client):
    """Test avec des champs manquants"""
    response = client.post('/auth/login',
                           data={'nom': '', 'password': ''},
                           follow_redirects=True)
    assert b'Tous les champs sont requis' in response.data



def test_login_invalid_credentials(client, app):
    """Test avec des identifiants invalides"""
    with app.app_context():
        # Crée un utilisateur avec un rôle
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw, role='utilisateur')
        db.session.add(user)
        db.session.commit()

        # Test mot de passe incorrect
        response = client.post('/auth/login',
                             data={'nom': 'testuser', 'password': 'mauvaispass'},
                             follow_redirects=True)
        assert b'Nom ou mot de passe incorrect' in response.data
        
        # Vérifie que la session est vide
        with client.session_transaction() as sess:
            assert 'user_id' not in sess

        # Test utilisateur inexistant
        response = client.post('/auth/login',
                             data={'nom': 'nonexistent', 'password': 'testpass123'},
                             follow_redirects=True)
        assert b'Nom ou mot de passe incorrect' in response.data
        
        # Vérifie que la session est vide
        with client.session_transaction() as sess:
            assert 'user_id' not in sess


def test_login_session_values(client, app):
    """Vérifie les valeurs de session après connexion"""
    with app.app_context():
        # Crée un utilisateur avec un rôle spécifique
        hashed_pw = generate_password_hash('adminpass')
        admin = Utilisateur(nom='admin', password=hashed_pw, role='admin')
        db.session.add(admin)
        db.session.commit()

        response = client.post('/auth/login',
                  data={'nom': 'admin', 'password': 'adminpass'},
                  follow_redirects=True)
        assert response.status_code == 200
        
        # Vérifie que les valeurs de session sont correctes
        with client.session_transaction() as sess:
            assert sess['user_id'] == admin.id
            assert sess['user_nom'] == 'admin'
            assert sess['user_role'] == 'admin'


def test_login_redirect_dashboard(client, app):
    """Test la redirection vers le dashboard après connexion"""
    with app.app_context():
        # Crée un utilisateur avec un rôle
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw, role='utilisateur')
        db.session.add(user)
        db.session.commit()

        # Test la redirection sans follow_redirects
        response = client.post('/auth/login',
                             data={'nom': 'testuser', 'password': 'testpass123'},
                             follow_redirects=False)
        
        assert response.status_code == 302
        assert response.headers['Location'].endswith('/dashboard')

        # Test la redirection avec follow_redirects
        response = client.post('/auth/login',
                             data={'nom': 'testuser', 'password': 'testpass123'},
                             follow_redirects=True)
        assert response.status_code == 200
        # Vérifie que nous sommes sur la page dashboard
        assert 'Tableau de bord'.encode() in response.data

import pytest 
from werkzeug.security import generate_password_hash




def test_login_page_get(client):
    """Test l'accès à la page de login (GET)"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Connexion' in response.data 


def test_login_success(client, app):
    """Test une connexion valide"""
    with app.app_context():
        # Crée un utilisateur de test
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw, role='utilisateur')
        db.session.add(user)
        db.session.commit()

        # Tente de se connecter
        response = client.post('/auth/login', 
                             data={'nom': 'testuser', 'password': 'testpass123'},
                             follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Connexion r' in response.data  # Message de succès
        assert 'user_id' in session  # Vérifie la session


def test_login_missing_fields(client):
    """Test avec des champs manquants"""
    response = client.post('/auth/login', 
                         data={'nom': '', 'password': ''},
                         follow_redirects=True)
    assert b'Tous les champs sont requis' in response.data




def test_login_invalid_credentials(client, app):
    """Test avec des identifiants invalides"""
    with app.app_context():
        # Crée un utilisateur
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # Test mot de passe incorrect
        response = client.post('/auth/login',
                             data={'nom': 'testuser', 'password': 'mauvaispass'},
                             follow_redirects=True)
        assert b'Nom ou mot de passe incorrect' in response.data

        # Test utilisateur inexistant
        response = client.post('/auth/login',
                             data={'nom': 'nonexistent', 'password': 'testpass123'},
                             follow_redirects=True)
        assert b'Nom ou mot de passe incorrect' in response.data



def test_login_session_values(client, app):
    """Vérifie les valeurs de session après connexion"""
    with app.app_context():
        # Crée un utilisateur avec un rôle spécifique
        hashed_pw = generate_password_hash('adminpass')
        admin = Utilisateur(nom='admin', password=hashed_pw, role='admin')
        db.session.add(admin)
        db.session.commit()

        client.post('/auth/login',
                  data={'nom': 'admin', 'password': 'adminpass'},
                  follow_redirects=True)
        
        with client.session_transaction() as sess:
            assert sess['user_id'] == admin.id
            assert sess['user_nom'] == 'admin'
            assert sess['user_role'] == 'admin'
            

def test_login_redirect_dashboard(client, app):
    """Test la redirection vers le dashboard après connexion"""
    with app.app_context():
        hashed_pw = generate_password_hash('testpass123')
        user = Utilisateur(nom='testuser', password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login',
                             data={'nom': 'testuser', 'password': 'testpass123'},
                             follow_redirects=False)
        
        assert response.status_code == 302
        assert '/dashboard' in response.location  # Vérifie la redirection

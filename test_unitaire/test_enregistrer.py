import pytest
from werkzeug.security import check_password_hash


def test_register_route_get(client):
    """Test l'accès à la page d'inscription (GET)"""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert 'Créer un compte' in response.data.decode('utf-8')  # Vérifie le titre de la page


def test_register_success(client, app):
    """Test une inscription valide"""
    with app.app_context():
        # Vérifie que la base est vide initialement
        assert Utilisateur.query.count() == 0

        data = {
            'nom': 'newuser',
            'password': 'ValidPass123',
            'confirm_password': 'ValidPass123'
        }
        
        response = client.post('/auth/register', 
                             data=data,
                             follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Compte cr' in response.data  # Message de succès
        
        # Vérification en base
        user = Utilisateur.query.filter_by(nom='newuser').first()
        assert user is not None
        assert check_password_hash(user.password, 'ValidPass123')
        assert user.role == 'utilisateur'  # Vérifie le rôle par défaut
 
def test_register_existing_user(client, init_db):
    """Test avec un nom d'utilisateur existant"""
    response = client.post('/auth/register', data={
        'nom': 'testuser',  # Utilisateur créé par init_db
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert b'Ce nom est d' in response.data  # Message d'erreur attendu




def test_register_invalid_data(client):
    """Test avec des données invalides"""
    test_cases = [
        # (data, expected_error_message)
        (
            {'nom': '', 'password': 'pwd', 'confirm_password': 'pwd'},
            b'Tous les champs sont requis'
        ),
        (
            {'nom': 'usr', 'password': 'pwd', 'confirm_password': 'pwd'},
            b'Le nom doit contenir au moins 4 caract'
        ),
        (
            {'nom': 'user@', 'password': 'pwd', 'confirm_password': 'pwd'},
            b'Le nom ne doit contenir que des lettres et chiffres'
        ),
        (
            {'nom': 'validuser', 'password': '123', 'confirm_password': '123'},
            b'Le mot de passe doit faire 8 caract'
        ),
        (
            {'nom': 'validuser', 'password': 'password123', 'confirm_password': 'different'},
            b'Les mots de passe ne correspondent pas'
        )
    ]
    
    for data, error_msg in test_cases:
        response = client.post('/auth/register', data=data)
        assert error_msg in response.data
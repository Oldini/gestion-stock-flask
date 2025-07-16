import pytest
from app import create_app, db

def test_accueil(client):
    """Test de la route d'accueil"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Bienvenue" in response.data


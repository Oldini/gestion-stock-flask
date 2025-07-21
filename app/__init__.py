from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.base import Config
from config.testing import TestingConfig
from flask_migrate import Migrate 
import os

# Initialisation de l'objet SQLAlchemy, mais pas encore lié à l'app
db = SQLAlchemy()

def create_app(config_class=None):
    app = Flask(__name__)

    # Choix de la configuration :
    # Si une config est passée manuellement, on l'utilise
    if config_class:
        app.config.from_object(config_class)
    else:
        # Sinon, on lit la variable d'environnement FLASK_ENV
        env = os.getenv('FLASK_ENV', 'production')
        if env == 'testing':
            app.config.from_object(TestingConfig)
        else:
            app.config.from_object(Config)

    # Connexion de SQLAlchemy à l'app
    db.init_app(app)

    #Connexion de Flask-Migrate à l'app et à SQLAlchemy
    migrate.init_app(app, db)
       

    # Création automatique des tables dans la base de données
    with app.app_context():
        db.create_all()

    # Importation et enregistrement des routes
    from app.routes import init_routes
    init_routes(app)

    return app




 

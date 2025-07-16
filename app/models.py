from . import db

# Table utilisateur
class Utilisateur(db.Model):  # Note la majuscule 'U' et db.Model
    __tablename__ = 'utilisateur' 

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Identifiant unique
    nom = db.Column(db.String(200), nullable=False)  # Nom de l'utilisateur
    password = db.Column(db.String(200), nullable=False)  # Mot de passe
    role = db.Column(db.String(20), nullable=False)  # admin ou simple utilisateur


# Table produit
class Produit(db.Model):  # Note la majuscule 'P' et db.Model
    __tablename__ = 'produit'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True) 
    nom = db.Column(db.String, nullable=False)  # Nom du produit
    prix = db.Column(db.Float, nullable=False)  # Prix du produit
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))  # Clé étrangère, note l'orthographe de la table

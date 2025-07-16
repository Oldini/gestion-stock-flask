import datetime
from flask import render_template,request,flash, redirect, session, url_for
from sqlalchemy import text
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Produit, Utilisateur
import traceback

def init_routes(app):

    @app.route('/')
    def accueil():
        return render_template('accueil.html')

    # Route de test pour vérifier la connexion
    @app.route('/test_db')
    def test_db():
        try:
            # Utilise text() pour les requêtes SQL brutes
            db.session.execute(text("SELECT 1"))
            return "La connexion à la base de données fonctionne !"
        except Exception as e:
            return f"Erreur de connexion à la base : {str(e)}"
        
     # Route pour enregister les donner
    @app.route('/auth/register', methods=['GET', 'POST'])
    def register():
        """Gère l'inscription des nouveaux utilisateurs"""

        
        
        if request.method == 'POST':
            # 1. Récupération des données du formulaire
            nom = request.form.get('nom').strip()  # Nettoyage des espaces
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # 2. Validation des données (couche sécurité)
            errors = []
            
            # 2.1 Vérification des champs obligatoires
            if not all([nom, password, confirm_password]):
                errors.append("Tous les champs sont requis")
            
            # 2.2 Validation du nom d'utilisateur
            elif len(nom) < 4:
                errors.append("Le nom doit contenir au moins 4 caractères")
            elif not nom.isalnum():  # Empêche les caractères spéciaux
                errors.append("Le nom ne doit contenir que des lettres et chiffres")
            
            # 2.3 Validation du mot de passe
            elif len(password) < 8:
                errors.append("Le mot de passe doit faire 8 caractères minimum")
            elif password != confirm_password:
                errors.append("Les mots de passe ne correspondent pas")

            # 3. Vérification de l'unicité du nom
            existing_user = Utilisateur.query.filter_by(nom=nom).first()
            if existing_user:
                errors.append("Ce nom est déjà utilisé")

            # 4. Gestion des erreurs
            if errors:
                print("Erreurs trouvées :", errors)  # 
                for error in errors:
                    flash(error, 'danger')
                return render_template('auth/register.html', nom=nom)

            # 5. Création du compte (si validation OK)
            try:
                print("Début de l'inscription")
                print(f"Données reçues: nom={nom}, password={password}")
                
                # Hashage du mot de passe
                hashed_pw = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
                print(f"Insertion de: {nom} | Hash: {hashed_pw[:10]}...")  # Affiche les 10 premiers caractères du hash

                # Création de l'utilisateur
                new_user = Utilisateur(nom=nom, password=hashed_pw, role='utilisateur')
                print("Utilisateur créé")

                # Ajout à la session
                db.session.add(new_user)
                print("Utilisateur ajouté à la session")

                # Commit
                db.session.commit()
                print("Commit réussi")
                
                # Vérification que l'utilisateur existe
                user = Utilisateur.query.filter_by(nom=nom).first()
                if user:
                    print("Utilisateur vérifié dans la base")
                    flash('Compte créé avec succès!', 'success')
                    return redirect(url_for('login'))
                else:
                    print("Erreur: Impossible de retrouver l'utilisateur après l'insertion")
                    flash("Erreur lors de la création du compte", 'danger')
                    return redirect(url_for('register'))

            except Exception as e:
                print(f"Erreur lors de l'inscription: {str(e)}")
                traceback.print_exc()
                db.session.rollback()
                flash("Erreur lors de la création du compte", 'danger')
                return redirect(url_for('register'))
        # GET: Affiche le formulaire vierge
        return render_template('auth/register.html')
    
      # Route pour connexion 

    @app.route('/auth/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            nom = request.form.get('nom')
            password = request.form.get('password')
            
            # 1. Vérification des champs
            if not nom or not password:
                flash('Tous les champs sont requis', 'danger')
                return redirect(url_for('login'))
            
            # 2. Recherche de l'utilisateur
            user = Utilisateur.query.filter_by(nom=nom).first()
            
            # 3. Vérification du mot de passe
            if not user or not check_password_hash(user.password, password):
                flash('Nom ou mot de passe incorrect', 'danger')
                return redirect(url_for('login'))
            
            # 4. Connexion réussie
            session['user_id'] = user.id  # Stocke l'ID en session
            session['user_nom'] = user.nom
            session['user_role'] = user.role
            
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))  # Redirige vers la page dashboard 
        
        return render_template('auth/login.html')
    





    
    
    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        try:
            # Récupérer tous les produits
            produits = Produit.query.all()
            
            # Passer les produits au template
            return render_template('dashboard.html', produits=produits)
        except Exception as e:
            flash(f"Erreur lors de la récupération des produits: {str(e)}", "danger")
            return render_template('dashboard.html', produits=[])

    @app.route('/modifier-produit/<int:id>', methods=['GET', 'POST'])
    def modifier_produit(id):
        """
        Route pour modifier un produit
        
        Args:
            id (int): L'ID du produit à modifier
        
        Returns:
            Response: Redirection vers le dashboard après modification
        """
        try:
            # Récupérer le produit
            produit = Produit.query.get_or_404(id)
            utilisateur_id = session.get('user_id')
            
            if request.method == 'POST':
                # Récupérer les données du formulaire
                nouveau_nom = request.form.get('nom')
                nouveau_prix = request.form.get('prix')
                
                # Valider les données
                if not nouveau_nom or not nouveau_prix:
                    flash("Tous les champs sont obligatoires", "danger")
                    return redirect(url_for('dashboard'))
                
                try:
                    # Convertir le prix
                    nouveau_prix = float(nouveau_prix)
                    if nouveau_prix <= 0:
                        flash("Le prix doit être supérieur à 0", "danger")
                        return redirect(url_for('dashboard'))
                except ValueError:
                    flash("Le prix doit être un nombre valide", "danger")
                    return redirect(url_for('dashboard'))
                
                # Mettre à jour le produit
                produit.nom = nouveau_nom
                produit.prix = nouveau_prix
                
                # Sauvegarder les modifications
                db.session.commit()
                flash("Produit modifié avec succès", "success")
                return redirect(url_for('dashboard'))
            
            # GET: Afficher le formulaire de modification
            return render_template('modifier_produit.html', produit=produit)
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la modification: {str(e)}", "danger")
            return redirect(url_for('dashboard'))

    @app.route('/supprimer-produit/<int:id>', methods=['GET'])
    def supprimer_produit(id):
        """
        Route pour supprimer un produit
        
        Args:
            id (int): L'ID du produit à supprimer
        
        Returns:
            Response: Redirection vers le dashboard après suppression
        """
        try:
            # Récupérer le produit
            produit = Produit.query.get_or_404(id)
            utilisateur_id = session.get('user_id')
            
            # Supprimer le produit
            db.session.delete(produit)
            db.session.commit()
            
            flash("Produit supprimé avec succès", "success")
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la suppression: {str(e)}", "danger")
            return redirect(url_for('dashboard'))
    







    @app.route('/logout')
    def logout():
        session.clear()  # vide la session (déconnexion)
        flash("Déconnexion réussie", "info")
        return redirect(url_for('login'))  # Redirige vers la page de login
    







    @app.route('/ajouter-produit', methods=['POST'])
    def ajouter_produit():
        nom = request.form.get('nom')
        prix = request.form.get('prix')

        # Validation des données
        if not nom or not prix:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for('dashboard'))

        try:
            # Vérification que le prix est un nombre valide
            prix = float(prix)  # Conversion en float
            if prix <= 0:
                flash("Le prix doit être supérieur à 0", "danger")
                return redirect(url_for('dashboard'))

            utilisateur_id = session.get('user_id')
            if utilisateur_id is None:
                flash("Utilisateur non connecté", "danger")
                return redirect(url_for('login'))

            # Création du produit
            nouveau = Produit(nom=nom, prix=prix, utilisateur_id=utilisateur_id)
            db.session.add(nouveau)
            db.session.commit()
            flash("Produit ajouté avec succès", "success")

        except ValueError:
            flash("Le prix doit être un nombre valide", "danger")
            db.session.rollback()
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout du produit: {str(e)}", "danger")

        return redirect(url_for('dashboard'))


## ⚙️ Pré-requis

- Python 3.11
- PostgreSQL (port 5432)

# 1. Installer PostgreSQL
sudo apt install postgresql postgresql-contrib

# 2. Lancer PostgreSQL et créer un utilisateur
sudo -u postgres psql

# 3. Dans PostgreSQL :
CREATE USER postgres WITH PASSWORD 'oldini031001';
CREATE DATABASE Stock;
CREATE DATABASE stock_test;
GRANT ALL PRIVILEGES ON DATABASE Stock TO postgres;
GRANT ALL PRIVILEGES ON DATABASE stock_test TO postgres;
\q

# 4. Copier le fichier d'exemple
cp .env .env

# 5. Adapter le mot de passe dans .env si besoin

# 6. Installer les dépendances
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 7. Lancer le projet
python run.py

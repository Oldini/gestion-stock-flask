from dotenv import load_dotenv
load_dotenv()

import os
print(">>> .env DATABASE_URL =", os.getenv("DATABASE_URL"))  # vérif .env

from app import create_app
app = create_app()

if __name__ == '__main__':
    print(">>> CONFIG DATABASE =", app.config.get("SQLALCHEMY_DATABASE_URI"))  # vérif config
    app.run(host=app.config["HOST"], port=app.config["PORT"])

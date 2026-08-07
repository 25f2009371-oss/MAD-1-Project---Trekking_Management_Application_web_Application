from flask import Flask
from models import db

app = None

def setup_app():
    global app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databse.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.app_context().push()
    print("Database setup done ... ")

setup_app()

if __name__ == "__main__":
    app.run(debug=True)

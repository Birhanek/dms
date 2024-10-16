from flask import Flask
from flask_login import LoginManager
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from os import path
from flask_cors import CORS

# Define the database URL
DATABASE_URL = 'sqlite:///dms.db'  # SQLite database in the current directory

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session instance
session = Session()

# Define the base class for the models
Base = declarative_base()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "qjauhste563hstnckolg"
    app.config['UPLOAD_FOLDER'] = "./uploads"

   
    #  local imports typically controllers
    from .auth import auth
    #  Registering those controllers in to the app
    app.register_blueprint(auth,url_prefix='/')
    from .models import User
    
    create_database(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    #login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return session.query(User).get(int(id))

    return app


def create_database (app):
    Base.metadata.create_all(engine)
    print("All tables are created!")
    
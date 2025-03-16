from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from config import Config
from model import mongo
from view import auth_bp

from os import path

bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__)
# Initialize extensions
  app.config.from_object(Config) 
  mongo.init_app(app)
  bcrypt.init_app(app)
  jwt.init_app(app)
  login_manager.init_app(app)
  # Register blueprints
  app.register_blueprint(auth_bp)
    
  return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
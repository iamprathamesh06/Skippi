from flask import Flask
from flask_login import LoginManager
from os import path

def create_app():
  app = Flask(__name__)
  
  return app
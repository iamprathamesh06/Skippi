import urllib.parse
from pymongo import MongoClient
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 1 hour

jwt = JWTManager(app)

# Encode special characters in username and password
username = urllib.parse.quote_plus("iamprathamesh")
password = urllib.parse.quote_plus("password")

# MongoDB Connection URI
uri = f"mongodb+srv://{username}:{password}@cluster0.uavqh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["skippi"]

from flask import Flask
from routes.auth import auth_bp
from config import app
from routes.private import private_bp 

app.register_blueprint(auth_bp)
app.register_blueprint(private_bp)

if __name__ == '__main__':
    app.run(debug=True)

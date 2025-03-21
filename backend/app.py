from flask import Flask
from routes.auth import auth_bp
from routes.course_routes import course_bp
from routes.article_routes import article_bp
from config import app

app.register_blueprint(auth_bp)
app.register_blueprint(course_bp)
app.register_blueprint(article_bp)

if __name__ == '__main__':
    app.run(debug=True)

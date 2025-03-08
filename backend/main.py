from mvc.app import create_app
from mvc.controller import views

app = create_app()
app.register_blueprint(views, url_prefix='/')

if __name__ == '__main__':
    app.run()
from flask import Flask

app = Flask(__name__)

def create_app():
    app.config.from_object('config.Config')
    from . import views
    return app
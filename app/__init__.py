from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_app():
    app.config.from_object('config.Config')
    from . import views
    return app
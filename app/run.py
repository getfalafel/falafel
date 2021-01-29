from flask import Flask
from flask_cors import CORS
from dynaconf import settings
from app.core import configuration


def construct(**config):
    app = Flask(__name__, static_folder=settings.get('STATIC_DIR'), template_folder=settings.get('VIEWS_DIR'))
    configuration.init_app(app, **config)
    CORS(app)
    return app


def create_app(**config):
    app = construct(**config)
    configuration.load_extensions(app)
    return app

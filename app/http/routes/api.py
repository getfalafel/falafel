from flask import Blueprint, jsonify, url_for
from app.http.controllers import ApiController

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return ApiController.index()


def init_app(app):
    app.register_blueprint(api)

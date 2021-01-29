from flask import Blueprint
from app.http.controllers import WebController

web = Blueprint('web', __name__)


@web.route("/", methods=['GET'])
def root():
    return WebController.index()


def init_app(app):
    app.register_blueprint(web)

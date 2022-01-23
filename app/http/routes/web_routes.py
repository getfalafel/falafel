from flask import Blueprint
from app.http.controllers import web_controller

web = Blueprint("web", __name__)


@web.route("/", methods=["GET"])
def index():
    return web_controller.index()


def init_app(app):
    app.register_blueprint(web)

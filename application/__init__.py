from flask import Flask
from flask_restful import Api
from application.api.users.UserController import UserController
from application.extensions import db, migrate


def create_app(config_name):

    app = Flask(__name__)
    configure_app(app, config_name)
    configure_hook(app)
    configure_blueprint(app)
    configure_extensions(app)

    @app.route("/")
    def hello_world():
        return "Trading Assistance"

    return app


def configure_app(app, config_name=None):
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def configure_blueprint(app):
    api = Api(app)
    api.add_resource(UserController, '/users')

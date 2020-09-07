from flask import Flask, jsonify
from application.api import api_blueprint
from application.api.stock.StockController import stock_api
from application.extensions import db, migrate, jwt
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions


def create_app(config_name):

    app = Flask(__name__)
    configure_app(app, config_name)
    configure_hook(app)
    configure_blueprint(app)
    configure_extensions(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

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
    # jwt.init_app(app)
    migrate.init_app(app, db)


def configure_blueprint(app):
    app.register_blueprint(api_blueprint)
    app.register_blueprint(stock_api)


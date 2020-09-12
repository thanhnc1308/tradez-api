from flask import Flask, jsonify
from flask_sqlalchemy import get_debug_queries
from application.api import api_blueprint
from application.api.mail.MailController import mail_api
from application.api.stock.StockController import stock_api
from application.api.auth.AuthController import auth_api
from application.extensions import db, migrate, jwt, mail
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
        return 'Trading Assistance'

    return app


def configure_app(app, config_name=None):
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)


def configure_hook(app):
    app.after_request(sql_debug)


def configure_extensions(app):
    db.init_app(app)
    # jwt.init_app(app)
    migrate.init_app(app, db)
    configure_mail_extension(app)  # this configuration must be before mail.init_app(app)
    mail.init_app(app)


def configure_blueprint(app):
    app.register_blueprint(api_blueprint)
    app.register_blueprint(stock_api)
    app.register_blueprint(mail_api)
    app.register_blueprint(auth_api)


def configure_mail_extension(app):
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'montoson138@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ACI13898'
    app.config['MAIL_DEFAULT_SENDER'] = 'Thanh NC'


def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n    ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(total_duration * 1000, 2))

    print('=' * 80)
    print('SQL Queries: - {0}\nQueries executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')
    return response

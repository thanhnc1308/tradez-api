from flask import Flask
from flask_sqlalchemy import get_debug_queries
from application.api.users.UserController import user_api
from application.api.stock.StockController import stock_api
from application.api.stock.StockPriceController import stock_price_api
from application.api.stock.StockScreenerController import stock_screener_api
from application.api.journal.JournalController import journal_api
from application.api.notifications.NotificationController import notification_api
from application.api.notifications.BLNotification import crawl_and_send_notification
from application.api.backtest.BacktestController import backtest_api
from application.api.auth.AuthController import auth_api
from application.extensions import db, migrate, jwt, mail, cors
from application.config import ProductionConfig
from werkzeug.exceptions import default_exceptions
import schedule
import time
import datetime
import uuid
import os
from multiprocessing import Process

t = None
os.environ['CRAWL_DATA_SCHEDUALING_TIME'] = '22:40'

def run_schedule():
    """ infinite loop for schedule """
    while 1:
        schedule.run_pending()
        time.sleep(1)

def create_app(config_name):

    app = Flask(__name__)
    configure_app(app, config_name)
    configure_hook(app)
    configure_blueprint(app)
    configure_extensions(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        return {
            "message": str(e)
        }

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    @app.route("/")
    def hello_world():
        return 'Trading Assistance'

    @app.route("/test")
    def test():
        return 'test ok'

    # http://localhost:5000/timer/on
    @app.route('/timer/<string:status>')
    def timer(status):
        global t
        if status == 'on' and not t:
            print("CRAWL_DATA_SCHEDUALING_TIME: ", os.environ.get("CRAWL_DATA_SCHEDUALING_TIME"))
            crawl_and_send_notification()
            # schedule.every().day.at(os.environ.get("CRAWL_DATA_SCHEDUALING_TIME")).do(crawl_and_send_notification)
            # schedule.every(nsec).seconds.do(run_job, str(uuid.uuid4()))
            t = Process(target=run_schedule)
            t.start()
            return "timer on"
        elif status == 'off' and t:
            if t:
                t.terminate()
                t = None
                schedule.clear()
            return "timer off\n"
        return "timer status not changed\n"

    # http://localhost:5000/crawl
    @app.route('/crawl')
    def crawl():
        crawl_and_send_notification()
        return 'ok'

    return app


def configure_app(app, config_name=None):
    # config_module = f"application.config.{config_name.capitalize()}Config"
    config_module = ProductionConfig
    app.config.from_object(config_module)


def configure_hook(app):
    # app.after_request(sql_debug)
    pass


def configure_extensions(app):
    db.init_app(app)
    # jwt.init_app(app)
    migrate.init_app(app, db)
    configure_mail_extension(app)  # this configuration must be before mail.init_app(app)
    mail.init_app(app)
    cors.init_app(app)


def configure_blueprint(app):
    app.register_blueprint(user_api)
    app.register_blueprint(stock_api)
    app.register_blueprint(stock_price_api)
    app.register_blueprint(stock_screener_api)
    app.register_blueprint(journal_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(notification_api)
    app.register_blueprint(backtest_api)


def configure_mail_extension(app):
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'montoson138@gmail.com'
    app.config['MAIL_PASSWORD'] = '12345678@Abc'
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

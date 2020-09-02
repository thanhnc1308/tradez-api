from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt import JWT
# from flask_cache import Cache

db = SQLAlchemy()
migrate = Migrate()
jwt = JWT()
# cache = Cache()

login_manager = LoginManager()
# login_manager.login_view = "main.login"
# login_manager.login_message_category = "warning"
#
#
# @login_manager.user_loader
# def load_user(userid):
#     return User.query.get(userid)
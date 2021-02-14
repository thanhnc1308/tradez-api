from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
# from flask_cache import Cache
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
# jwt = JWT()
jwt = JWTManager()
mail = Mail()
# cache = Cache()
cors = CORS()

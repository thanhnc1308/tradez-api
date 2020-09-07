from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT
# from flask_cache import Cache

db = SQLAlchemy()
migrate = Migrate()
jwt = JWT()
# cache = Cache()

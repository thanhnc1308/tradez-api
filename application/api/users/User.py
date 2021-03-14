from application.extensions import db
from application.api.base.BaseModel import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from datetime import timedelta
from flask import current_app


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    facebook = db.Column(db.String(100), unique=True)
    telegram = db.Column(db.String(100), unique=True)

    __mapper_args__ = {
        "order_by": username
    }

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        self.set_password(kwargs.get('password'))

    @property
    def raw_password(self):
        return None

    @raw_password.setter
    def raw_password(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # return True
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def __repr__(self):
        return "<User %s>" % self.username

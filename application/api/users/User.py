from application.extensions import db
from application.api.base.BaseModel import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash


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
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return "<User %s>" % self.username

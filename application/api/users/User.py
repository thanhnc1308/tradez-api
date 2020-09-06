from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from application.api.base.BaseModel import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    facebook = db.Column(db.String(100), unique=True)
    telegram = db.Column(db.String(100), unique=True)

    __mapper_args__ = {
        "order_by": username
    }

    # trading_logs = db.relationship('trading_log', backref='users', lazy='select')
    # emails = db.relationship("ContactEmail", back_populates="contact", cascade="all, delete-orphan")

    def __init__(self, username, email, password, facebook, telegram, **kwargs):
        db.Model.__init__(
            self,
            username=username,
            email=email,
            raw_password=password,
            facebook=facebook,
            telegram=telegram,
            **kwargs
        )
        self.set_password(password)

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
    def get_by_id(cls, user_id):
        """
        :rtype: object
        :type user_id: int
        """
        try:
            return User.query.filter_by(id=user_id).one()
        except Exception as e:
            return str(e)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User %s>" % self.username

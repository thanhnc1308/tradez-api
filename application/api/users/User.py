from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    facebook = db.Column(db.String(100), unique=True)
    telegram = db.Column(db.String(100), unique=True)

    def __init__(self, username, email, password, facebook, telegram, id=uuid.uuid4()):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.facebook = facebook
        self.telegram = telegram

    def __repr__(self):
        return "<User %s>" % self.username

    def save(self):
        db.session.add(self)
        db.session.commit()

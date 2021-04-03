from application.extensions import db
from application.api.base.BaseModel import BaseModel
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON

class Notification(BaseModel):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(UUID(as_uuid=True))
    condition_key = db.Column(JSON)
    condition_description = db.Column(db.String())
    description = db.Column(db.String())
    gmail = db.Column(db.String())
    tg_chat_id = db.Column(db.String())
    send_gmail = db.Column(db.Boolean())
    send_telegram = db.Column(db.Boolean())

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return "<Notification %s>" % self.index



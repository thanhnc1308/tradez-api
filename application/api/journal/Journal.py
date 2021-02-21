from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from application.api.base.BaseModel import BaseModel


class Journal(BaseModel):
    __tablename__ = "journal"
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(UUID(as_uuid=True))
    transaction_date = db.Column(db.Date)
    symbol = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10)) # win/lose
    quantity = db.Column(db.Numeric)
    entry = db.Column(db.Numeric)
    exit = db.Column(db.Numeric)
    total_value = db.Column(db.Numeric)
    pnl = db.Column(db.Numeric)
    screenshot = db.Column(db.String())
    comments = db.Column(db.String())

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return "<Stock %s>" % self.index


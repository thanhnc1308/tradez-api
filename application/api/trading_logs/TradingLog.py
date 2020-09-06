from application.extensions import db
from application.api.base.BaseModel import BaseModel, ReferenceCol
import uuid
from sqlalchemy.dialects.postgresql import UUID


class TradingLog(BaseModel):
    __tablename__ = 'trading_log'
    # Define a foreign key relationship to a User object
    user_id = ReferenceCol('users')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    entry = db.Column(db.Float, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

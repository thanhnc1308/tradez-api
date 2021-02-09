from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from application.api.base.BaseModel import BaseModel


class Stock(BaseModel):
    __tablename__ = "stock"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(), nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return "<Stock %s>" % self.index

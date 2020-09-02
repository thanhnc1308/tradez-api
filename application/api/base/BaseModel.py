from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created_date = db.Column()
    modified_date = db.Column()

    def __init__(self, _id, created_date, modified_date):
        self.id = _id
        self.created_date = created_date
        self.modified_date = modified_date



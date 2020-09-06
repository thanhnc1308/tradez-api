from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get_by_id(cls, id):
        # TODO: check type of id is uuid
        if not id:
            raise ValueError('id is not valid')
        return cls.query.get(id)  # TODO: parse uuid value of id

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.items():
            # Flask-RESTful makes everything None by default
            if value is not None:
                setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class BaseModel(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


# class SurrogatePK(object):
#     """A mixin that adds a surrogate integer 'primary key' column named
#     ``id`` to any declarative-mapped class.
#     """
#     __table_args__ = {'extend_existing': True}
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     @classmethod
#     def get_by_id(cls, id):
#         if id <= 0:
#             raise ValueError('ID must not be negative or zero!')
#         if any(
#             (isinstance(id, basestring) and id.isdigit(),
#              isinstance(id, (int, float))),
#         ):
#             return cls.query.get(int(id))
#         return None


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.
    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)  # pragma: no cover

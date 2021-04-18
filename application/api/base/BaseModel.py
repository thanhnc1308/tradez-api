from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """
    @classmethod
    def execute(cls, sql):
        # TODO: check sql injection
        result = db.engine.execute(sql)
        return result

    @classmethod
    def execute_scalar(cls, sql):
        # TODO: check sql injection
        result = db.engine.execute(sql).scalar()
        return result

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get_all(cls, order_by='updated_at', **kwargs):
        # return cls.query.all()
        return cls.query.filter_by(**kwargs).order_by(order_by).all()

    @classmethod
    def count_all(cls):
        return cls.query.count()

    @classmethod
    def get_by_id(cls, _id):
        # TODO: check type of id is uuid
        if not _id:
            raise ValueError('id is not valid')
        return cls.query.get(_id)  # TODO: parse uuid value of id

    @classmethod
    def find_latest(cls):
        return cls.query.order_by(cls.updated_at.desc()).first()

    @classmethod
    def find_by_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def find_and_order_by(cls, order_by='updated_at', **kwargs):
        return cls.query.filter_by(**kwargs).order_by(order_by).all()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_all_omit_record_with_this_id(cls, _id):
        return cls.query.filter(cls.id != _id).all()

    @classmethod
    def find_all_omit_record_with_this_slug(cls, slug):
        return cls.query.filter(cls.slug != slug).all()

    @classmethod
    def find_first_omit_record_with_this_name(cls, _id, name):
        return cls.query.filter_by(name=name).filter(cls.id != _id).first()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        # Set latest updated_at
        kwargs['updated_at'] = db.func.now()
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

    """ Utility functions """
    # @classmethod
    # def make_slug(cls, slug):
    #     return slugify(slug)

    @classmethod
    def date_to_string(cls, raw_date):
        return "{}".format(raw_date)


class BaseModel(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # __mapper_args__ = {
    #     "order_by": created_at
    # }


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.
    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)  # pragma: no cover


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

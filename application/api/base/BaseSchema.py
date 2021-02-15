from webargs.flaskparser import use_args, use_kwargs
from marshmallow import Schema, fields
from application.api.base.PagingSchema import PagingSchema


class BaseSchema(Schema):
    __abstract__ = True

    id = fields.UUID()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @classmethod
    def validate_fields(cls, args_type=None, schema_kwargs=None, **kwargs):
        schema_kwargs = schema_kwargs or {}

        def factory(request):
            # Filter based on 'fields' query parameter
            only = request.args.get('fields', None)
            # Respect partial updates for PATCH requests
            partial = request.method == 'PUT'
            # Add current request to the schema's context
            # and ensure we're always using strict mode
            return cls(
                only=only, partial=partial, strict=True,
                context={'request': request}, **schema_kwargs
            )

        if args_type == 'use_kwargs':
            return use_kwargs(factory, **kwargs)
        return use_args(factory, **kwargs)


class BaseListSchema(Schema):
    __abstract__ = True

    items = fields.List(fields.Nested(BaseSchema()))
    meta = fields.Nested(PagingSchema())


class SluggableSchema(BaseSchema):
    slug = fields.String(dump_only=True)



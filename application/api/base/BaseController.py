from flask import make_response, jsonify, abort, request, url_for
from flask_restful import Resource
from application.helpers import paginate
from http import HTTPStatus
from marshmallow import ValidationError
import traceback
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseController(Resource):
    model = None
    schema = None

    def get(self, id=None):
        try:
            data = self.model.get_by_id(id)
            if not data:
                abort(404, "Not found")
            return self.schema.dump(data), HTTPStatus.OK
        except Exception as e:
            return {
                'error': str(e)
            }

    def put(self, id):
        data = self.model.query.filter_by(id=id).first()
        if not data:
            abort(404, "Not found")
        errors = self.schema.validate(request.form)
        if errors:
            abort(HTTPStatus.BAD_REQUEST, str(errors))
        data.update(**request.form)
        return self.schema.dump(data)

    def delete(self, id):
        data = self.model.query.filter_by(id=id).first()
        if not data:
            abort(404, "Not found")
        data.delete()
        return make_response(
            jsonify(id)
        )


class BaseListController(Resource):
    model = None
    list_schema = None

    def get(self):
        try:
            data = self.model.get_all()
            return self.list_schema.dump(data)
        except Exception as e:
            logger.exception(e)
            # print(traceback.format_exc())
            # traceback.print_exc()
            # traceback.print_stack()
            # print(sys.exc_info()[2])
            return make_response(
                str(e)
            )

    def post(self):
        try:
            print(request.form)
            errors = self.schema.validate(request.form)
            if errors:
                abort(HTTPStatus.BAD_REQUEST, str(errors))
            new_item = self.model.create(**request.form)
            return {
                'user': self.schema.dump(new_item)
            }
        except ValidationError as e:
            return {
                'message': str(e.valid_data)
            }
        except Exception as e:
            return {
                'message': str(e)
            }


class BasePagingController(Resource):
    model = None
    paging_schema = None

    def get(self):
        max_per_page = 10
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)

        p = self.model.query.paginate(page, per_page)

        meta = {
            'page': page,
            'per_page': per_page,
            'total': p.total,
            'pages': p.pages,
        }

        links = {}
        if p.has_next:
            links['next'] = url_for(request.endpoint, page=p.next_num,
                                    per_page=per_page)
        if p.has_prev:
            links['prev'] = url_for(request.endpoint, page=p.prev_num,
                                    per_page=per_page)
        links['first'] = url_for(request.endpoint, page=1,
                                 per_page=per_page)
        links['last'] = url_for(request.endpoint, page=p.pages,
                                per_page=per_page)

        meta['links'] = links
        result = {
            'items': p.items,
            'meta': meta
        }

        return self.paging_schema.dump(result), 200

    # @paginate(schema=paging_schema, max_per_page=10)
    # def get(self):
    #     try:
    #         data = self.model.query
    #         return data
    #     except Exception as e:
    #         logger.exception(e)
    #         # print(traceback.format_exc())
    #         # traceback.print_exc()
    #         # traceback.print_stack()
    #         # print(sys.exc_info()[2])
    #         return make_response(
    #             str(e)
    #         )

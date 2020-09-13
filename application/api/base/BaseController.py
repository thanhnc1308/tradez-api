from flask import make_response, jsonify, abort, request, url_for
from flask_restful import Resource
from http import HTTPStatus
from application.helpers import get_error_response


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
            return get_error_response(e)

    def put(self, id):
        try:
            data = self.model.query.filter_by(id=id).first()
            if not data:
                abort(404, "Not found")
            errors = self.schema.validate(request.form)
            if errors:
                abort(HTTPStatus.BAD_REQUEST, str(errors))
            data.update(**request.form)
            return self.schema.dump(data)
        except Exception as e:
            return get_error_response(e)

    def delete(self, id):
        try:
            data = self.model.query.filter_by(id=id).first()
            if not data:
                abort(404, "Not found")
            data.delete()
            return make_response(
                jsonify(id)
            )
        except Exception as e:
            return get_error_response(e)


class BaseListController(Resource):
    model = None
    schema = None
    list_schema = None
    paging_schema = None

    def get(self):
        paging_filter = request.args.get('paging_filter', 1, type=int)
        try:
            if paging_filter == 1:
                return self.get_paging()
            else:
                # build query
                # filters = []
                # for conditions in query:
                #     if conditions[0] == 'id':
                #         filters.append(Member.id.in_(conditions[1].split(',')))
                #     else:
                #         for term in conditions[1].split(','):
                #             filters.append(Member.__dict__[conditions[0]].ilike('%' + term + '%'))
                # members = Member.query.filter(or_(*filters))
                # db.users.filter(or_(db.users.name == 'Ryan', db.users.country == 'England'))
                data = self.model.get_all()
                return self.list_schema.dump(data)
        except Exception as e:
            return get_error_response(e)

    def get_paging(self):
        max_per_page = 100
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

    def post(self):
        try:
            errors = self.schema.validate(request.form)
            if errors:
                abort(HTTPStatus.BAD_REQUEST, str(errors))
            new_item = self.model.create(**request.form)
            return {
                'data': self.schema.dump(new_item)
            }
        except Exception as e:
            return get_error_response(e)

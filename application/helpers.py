#!/usr/bin/env python3

import functools
from flask import request, url_for


def paginate(schema=None, max_per_page=100):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', max_per_page,
                                            type=int),
                           max_per_page)

            query = func(*args, **kwargs)
            p = query.paginate(page, per_page)

            meta = {
                'page': page,
                'per_page': per_page,
                'total': p.total,
                'pages': p.pages,
            }

            links = {}
            if p.has_next:
                links['next'] = url_for(request.endpoint, page=p.next_num,
                                        per_page=per_page, **kwargs)
            if p.has_prev:
                links['prev'] = url_for(request.endpoint, page=p.prev_num,
                                        per_page=per_page, **kwargs)
            links['first'] = url_for(request.endpoint, page=1,
                                     per_page=per_page, **kwargs)
            links['last'] = url_for(request.endpoint, page=p.pages,
                                    per_page=per_page, **kwargs)

            meta['links'] = links
            result = {
                'items': p.items,
                'meta': meta
            }

            return result, 200
        return wrapped
    return decorator


# def standardize_api_response(function):
#     """ Creates a standardized response. This function should be used as a deco
#     rator.
#     use @helpers.standardize_api_response above the function
#     :function: The function decorated should return a dict with one of
#     the keys  bellow:
#         success -> GET, 200
#         error -> Bad Request, 400
#         created -> POST, 201
#         updated -> PUT, 200
#         deleted -> DELETE, 200
#         no-data -> No Content, 204
#
#     :returns: json.dumps(response), staus code
#     """
#
#     available_result_keys = [
#         'success', 'error', 'created', 'updated', 'deleted', 'no-data']
#
#     status_code_and_descriptions = {
#         'success': (200, 'Successful Operation'),
#         'error': (400, 'Bad Request'),
#         'created': (201, 'Successfully created'),
#         'updated': (200, 'Successfully updated'),
#         'deleted': (200, 'Successfully deleted'),
#         'no-data': (204, '')
#     }
#
#     @functools.wraps(function)
#     def make_response(*args, **kwargs):
#
#         result = function(*args, **kwargs)
#
#         if not set(available_result_keys) & set(result):
#             raise ValueError('Invalid result key.')
#
#         status_code, description = status_code_and_descriptions[
#             next(iter(result.keys()))
#         ]
#
#         status_code = ('status_code', status_code)
#         description = (
#             ('description', description) if status_code[1] != 400 else
#             ('error', description)
#         )
#         data = (
#             ('data', next(iter(result.values()))) if status_code[1] != 204 else
#             ('data', '')
#         )
#
#         return json.dumps(collections.OrderedDict([
#             status_code, description, data])), status_code[-1]
#
#     return make_response

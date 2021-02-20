#!/usr/bin/env python3
from flask import request, url_for, jsonify
import jwt
from functools import wraps
from application.api.users.User import User
from application.api.users.UserSchema import user_schema


def verify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if token is None:
            return {"message": "Token is missing"}, 401
        try:
            data = jwt.decode(token, 'SECRET_KEY')  # app.config['SECRET_KEY']
            username = data.get('user')
            current_user = User.get_by_username(username)
            return f(user_schema.dump(current_user), *args, **kwargs)
        except Exception as e:
            return {"message": "Invalid user"}, 401
    return decorator


def paginate(schema=None, max_per_page=100):
    def decorator(func):
        @wraps(func)
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

            return schema.dump(result), 200
        return wrapped
    return decorator

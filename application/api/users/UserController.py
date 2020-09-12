from application.api.users.User import User
from application.api import api
from application.api.users.UserSchema import user_schema, user_paging_schema
from application.api.base.BaseController import BaseController, BaseListController
from application.helpers import paginate
from flask import make_response
from application.helpers import verify_token


def is_an_available_username(username):
    """Verify if an username is available.
    :username: a string object
    :returns: True or False
    """
    return User.query.filter_by(username=username).first() is None


class UserController(BaseController):
    model = User
    schema = user_schema


class UserListController(BaseListController):
    model = User
    schema = user_schema
    paging_schema = user_paging_schema

    @paginate(schema=user_paging_schema, max_per_page=10)
    # @verify_token
    def get(self):
        try:
            users = User.query
            return users
        except Exception as e:
            return make_response(
                str(e)
            )


api.add_resource(UserController, '/users/<string:id>', '/users/<username>', endpoint='user')
api.add_resource(UserListController, '/users', endpoint='users')

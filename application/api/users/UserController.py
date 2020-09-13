from flask import Blueprint
from flask_restful import Api
from application.api.users.User import User
from application.api.users.UserSchema import user_schema, users_schema, users_paging_schema
from application.api.base.BaseController import BaseController, BaseListController, BasePagingController
from application.helpers import paginate
from flask import make_response
from application.helpers import verify_token

user_api = Blueprint("user_api", __name__, url_prefix='/api/users')
api = Api(user_api)


class UserController(BaseController):
    model = User
    schema = user_schema


api.add_resource(UserController, '/<string:id>', endpoint='user')


class UserListController(BaseListController):
    model = User
    list_schema = users_schema


api.add_resource(UserListController, '', endpoint='users')


class UserPagingController(BasePagingController):
    model = User
    paging_schema = users_paging_schema

    # @paginate(schema=users_paging_schema, max_per_page=10)
    # # @verify_token
    # def get(self):
    #     try:
    #         users = User.query
    #         return users
    #     except Exception as e:
    #         return make_response(
    #             str(e)
    #         )


api.add_resource(UserPagingController, '/paging_filter', endpoint='users_paging_filter')

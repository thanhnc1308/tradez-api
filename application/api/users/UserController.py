from flask import Blueprint
from flask_restful import Api
from application.api.users.User import User
from application.api.users.UserSchema import user_schema, users_schema, users_paging_schema
from application.api.base.BaseController import BaseController, BaseListController

user_api = Blueprint("user_api", __name__, url_prefix='/api/users')
api = Api(user_api)


class UserController(BaseController):
    model = User
    schema = user_schema


api.add_resource(UserController, '/<string:id>', endpoint='user')


class UserListController(BaseListController):
    model = User
    schema = user_schema
    list_schema = users_schema
    paging_schema = users_paging_schema


api.add_resource(UserListController, '', endpoint='users')

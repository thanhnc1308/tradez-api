from flask import g, make_response, jsonify, abort, request
from flask_restful import Resource, reqparse, fields, marshal, marshal_with
from application.api.users.User import User
from application.api import api, meta_fields
from application.api.users.UserSchema import user_schema, users_schema
from application.helpers import paginate
from http import HTTPStatus
from flask_jwt import jwt_required

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
    'facebook': fields.String,
    'telegram': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

user_list_fields = {
    'items': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields),
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)
user_parser.add_argument('email', type=str)
user_parser.add_argument('facebook', type=str)
user_parser.add_argument('telegram', type=str)


def is_an_available_username(username):
    """Verify if an username is available.
    :username: a string object
    :returns: True or False
    """
    return User.query.filter_by(username=username).first() is None


class UserController(Resource):
    def get(self, id=None, username=None):
        try:
            user = None
            if username is not None:
                user = User.get_by_username(username)
            else:
                user = User.get_by_id(id)
            # user = User.query.get_or_404(id)
            # user = User.query.filter_by(username=username).first_or_404()
            if not user:
                abort(404, message="Not found")
            return user_schema.dump(user), HTTPStatus.OK
        except Exception as e:
            return {
                'error': str(e)
            }

    def put(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, "Not found")
        args = user_parser.parse_args()
        user.update(**args)
        # user = User.query.get_or_404(id)
        return user_schema.dump(user)

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, "Not found")
        user.delete()
        return make_response(
            jsonify(id)
        )


class UserListController(Resource):
    @marshal_with(user_list_fields)
    @paginate()
    def get(self):
        try:
            # users = User.query.all()
            users = User.query
            return users
        except Exception as e:
            return make_response(
                str(e)
            )

    def post(self):
        try:
            args = user_parser.parse_args()
            # check if username is available
            # if is_an_available_username(username=args['username'])
            new_user = User.create(**args)
            # errors = user_schema.validate(request.form)
            # if errors:
            #     abort(400, str(errors))
            # new_user = User(
            #     username=request.form.get('username'),
            #     email=request.form.get('email'),
            #     password=request.form.get('password'),
            #     facebook=request.form.get('facebook'),
            #     telegram=request.form.get('telegram')
            # )
            # db.session.add(new_user)
            # db.session.commit()
            return {
                'user': marshal(new_user, user_fields)
            }
        except Exception as e:
            return {
                'message': str(e)
            }


api.add_resource(UserController, '/user/<string:id>', '/user/<username>', endpoint='user')
api.add_resource(UserListController, '/users', endpoint='users')

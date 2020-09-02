from flask import make_response, jsonify, abort, request
from flask_restful import Resource, reqparse, fields, marshal
from application.api.users.User import User
from application.extensions import db

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
    'facebook': fields.String,
    'telegram': fields.String
}


class UserController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('facebook', type=str)
        self.parser.add_argument('telegram', type=str)
        super(UserController, self).__init__()

    def get(self, id):
        try:
            user = User.query.get_or_404(id)
            return {
                'user': marshal(user, user_fields)
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    def put(self, id):
        args = self.parser.parse_args()
        user = User.query.get_or_404(id)
        if 'email' in args:
            user.email = args['email']
        if 'username' in args:
            user.username = args['username']
        if 'password' in args:
            user.password = args['password']
        if 'facebook' in args:
            user.facebook = args['facebook']
        if 'telegram' in args:
            user.telegram = args['telegram']
        db.session.commit()
        return {
            'user': marshal(user, user_fields)
        }

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return make_response(
            jsonify(id)
        )



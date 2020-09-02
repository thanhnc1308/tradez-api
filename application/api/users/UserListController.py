from flask import make_response, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from application.api.users.User import User
from core.ResponseMessage import ResponseMessage
from application.extensions import db

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'facebook': fields.String,
    'telegram': fields.String
}


class UserListController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'username',
            type=str,
            required=True,
            help='Username is required!'
        )
        self.parser.add_argument(
            'password',
            type=str,
            required=True,
            help='Username is required!'
        )
        self.parser.add_argument(
            'email',
            type=str,
            required=True,
            help='Username is required!'
        )
        self.parser.add_argument('facebook', type=str)
        self.parser.add_argument('telegram', type=str)
        super(UserListController, self).__init__()

    def get(self):
        try:
            users = User.query.all()
            return {
                'users': marshal(users, user_fields)
            }
        except Exception as e:
            return make_response(
                jsonify(e)
            )

    def post(self):
        try:
            args = self.parser.parse_args()
            new_user = User(
                username=args['username'],
                email=args['email'],
                password=args['password'],
                facebook=args['facebook'],
                telegram=args['telegram']
            )
            db.session.add(new_user)
            db.session.commit()
            return {
                'user': marshal(new_user, user_fields)
            }
        except Exception as e:
            return {
                'message': str(e)
            }

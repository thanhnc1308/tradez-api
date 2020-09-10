from flask import Blueprint
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from application.api.users.User import User
from application.api.users.UserSchema import UserSchema, user_schema
from application.api import api

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')


@auth_api.route('/register', methods=['POST'])
def register():
    pass


@auth_api.route('/login', methods=['POST'])
def login():
    pass


# ref: https://github.com/solnsumei/flask-rest-api-setup
class Register(Resource):
    @staticmethod
    @UserSchema.validate_fields(locations=('json',))
    def post(args):

        if not safe_str_cmp(args['password'], args['password_confirmation']):
            return {
                'success': False,
                'errors': {
                    'password': ['Password and password confirmation do not match']}
            }, 409

        user = User.find_by_email(args['email'])
        if user:
            return {
                'success': False,
                'error': 'Email has already been taken'
            }, 409

        is_admin = False
        if User.count_all() < 1:
            is_admin = True

        phone = None

        if 'phone' in args:
            phone = args['phone']

        hashed_password = User.generate_hash(args['password'])

        user = User(args['name'], hashed_password, args['email'], phone, is_admin)
        user.save_to_db()

        return {
            'success': True,
            'user': user_schema.dump(user).data
        }, 201


api.add_resource(Register, '/signup')
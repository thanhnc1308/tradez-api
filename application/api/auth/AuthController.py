from flask import Blueprint, request, jsonify, make_response
import jwt
import json
import datetime
from application.api.base.ServiceResponse import ServiceResponse
from application.api.users.User import User
from application.api.users.UserSchema import user_schema

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')


@auth_api.route('/register', methods=['POST'])
def register():
    res = ServiceResponse()
    try:
        data = request.form
        user_schema.validate(data)
        # if username is None or password is None:
        #     abort(400)  # missing arguments
        # if User.query.filter_by(username=username).first() is not None:
        #     abort(400)  # existing user
        new_user = User.create(**data)
        if new_user:
            res.on_success(data=user_schema.dump(new_user))
        else:
            res.on_error(code=99, user_message='Error when create new user')
    except Exception as ex:
        res.on_exception(ex)
    return res.build()

@auth_api.route('/login', methods=['POST'])
def login():
    res = ServiceResponse()
    try:
        auth = json.loads(request.data)
        username = auth.get('username')
        password = auth.get('password')
        if not auth or username is None or password is None:
            res.on_error(code=401, user_message='Please enter username and password')

        # check if user exists
        user = User.get_by_username(username)
        if not user:
            res.on_error(code=401, user_message='Username does not exist')

        # check password here
        if user.check_password(password):
            token = jwt.encode({
                'user': username,  # it's better to return a public_id field here
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*7)
            }, 'SECRET_KEY')  # app.config['SECRET_KEY']
            res.on_success(data=token.decode('UTF-8'))
        else:
            res.on_error(code=401, user_message='Password is not correct')
    except Exception as ex:
        res.on_exception(ex)
    return res.build()

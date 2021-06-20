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
        auth = json.loads(request.data)
        email = auth.get('email')
        username = auth.get('username')
        password = auth.get('password')
        if not auth or username is None or password is None:
            res.on_error(code=99, user_message='Please enter username and password')
            return res.build()
        user = None
        # check if email exists
        user = User.get_by_email(email)
        if user != None:
            res.on_error(code=99, user_message='Email existed')
            return res.build()

        # check if user exists
        user = User.get_by_username(username)
        if user != None:
            res.on_error(code=99, user_message='Username existed')
            return res.build()

        new_user = User.create(**auth)
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
            res.on_error(code=99, user_message='Please enter username and password')
            return res.build()

        # check if user exists
        user = User.get_by_username(username)
        if not user:
            res.on_error(code=99, user_message='Username does not exist')
            return res.build()

        # check password here
        if user.check_password(password):
            token = jwt.encode({
                'user': username,  # it's better to return a public_id field here
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*7)
            }, 'SECRET_KEY')  # app.config['SECRET_KEY']
            print('token', token)
            if hasattr(token, 'decode'):
                print('token jwt')
                res.on_success(data=token.decode('UTF-8'))
            else:
                print('token string')
                res.on_success(data=token)
        else:
            res.on_error(code=99, user_message='Password is not correct')
    except Exception as ex:
        res.on_exception(ex)
    return res.build()

@auth_api.route('/user_info', methods=['POST'])
def user_info():
    res = ServiceResponse()
    try:
        auth = json.loads(request.data)
        token = auth.get('token')

        try:
            data = jwt.decode(token, options={"verify_signature": False})  # app.config['SECRET_KEY']
            username = data.get('user')
            current_user = User.get_by_username(username)
            print('current_user', user_schema.dump(current_user))
            res.on_success(data=user_schema.dump(current_user))
        except Exception as e:
            res.on_success(data={})
    except Exception as ex:
        res.on_exception(ex)
    return res.build()

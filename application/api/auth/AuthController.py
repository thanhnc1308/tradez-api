from flask import Blueprint, request, jsonify, make_response
import jwt
import datetime
from application.api.users.User import User
from application.api.users.UserSchema import user_schema

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')


@auth_api.route('/register', methods=['POST'])
def register():
    data = request.form
    user_schema.validate(data)
    # if username is None or password is None:
    #     abort(400)  # missing arguments
    # if User.query.filter_by(username=username).first() is not None:
    #     abort(400)  # existing user
    new_user = User.create(data)
    return {
        'success': True,
        'data': user_schema.dump(new_user)
    }, 201


@auth_api.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(
            'Could not verify',
            401,
            {
                'WWW-Authenticate': 'Basic realm="Login required"'
            }
        )

    # check if user exists
    user = User.get_by_username(auth.username)
    if not user:
        return make_response(
            'Could not verify',
            401,
            {
                'WWW-Authenticate': 'Basic realm="Login required"'
            }
        )

    # check password here
    if user.check_password(auth.password):
        token = jwt.encode({
            'user': request.authorization.username,  # it's better to return a public_id field here
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, 'SECRET_KEY')  # app.config['SECRET_KEY']
        return jsonify({
            'token': token.decode('UTF-8')
        })

    return make_response(
        'Could not verify',
        401,
        {
            'WWW-Authenticate': 'Basic realm="Login required"'
        }
    )

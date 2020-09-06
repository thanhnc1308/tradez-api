from flask import current_app
import datetime
from application.api.users.User import User


def set_jwt_handlers(jwt):
    """Define handlers to jwt.
    :jwt: flask_jwt.JWT object
    :returns: None
    """
    @jwt.authentication_handler
    def authenticate(username, password):
        user = User.objects(username=username).first()

        if user and User.check_password(password):
            return user
        return None

    @jwt.error_handler
    def error_handler(error):
        return 'Auth Failed: {}'.format(error.description), 400

    @jwt.payload_handler
    def make_payload(user):
        return {
            'user_id': str(user.id),
            'exp': (datetime.datetime.utcnow() +
                    current_app.config['JWT_EXPIRATION_DELTA']).isoformat()
        }

    @jwt.user_handler
    def load_user(payload):
        return User.objects(id=payload['user_id']).first()
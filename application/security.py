from application.api.users.User import User


def authenticate(email, password):
    user = User.find_by_email(email)
    if user and User.verify_hash(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

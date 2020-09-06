#!/usr/bin/env python

import functools
from flask import g, abort
from application.extensions import auth
from application.api.users.User import User


@auth.verify_password
def verify_password(username, password):
    """Validate user passwords and store user in the 'g' object"""
    print('username: ', username)
    print('password: ', password)
    g.user = User.query.filter_by(username=username).first()
    return g.user is not None and g.user.check_password(password)


def self_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('username', None):
            if g.user.username != kwargs['username']:
                abort(403)
        if kwargs.get('user_id', None):
            if g.user.id != kwargs['user_id']:
                abort(403)
        return func(*args, **kwargs)
    return wrapper

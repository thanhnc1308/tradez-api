# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

import string
import random
import os

from datetime import datetime
# import bson
#
#
# def is_a_valid_object_id(object_id):
#     """Verify if the value is valid as an object id.
#     :object_id: a string object
#     :returns: True or False
#     """
#     return bson.objectid.ObjectId.is_valid(object_id)


# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Model
STRING_LEN = 64


def get_current_time():
    return datetime.utcnow()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_AVATAR_EXTENSIONS


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e
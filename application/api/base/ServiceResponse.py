from flask import jsonify
from datetime import datetime
from werkzeug.exceptions import HTTPException
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ServiceResponse:
    def __init__(self, code=200, data=None, user_message="", system_message=""):
        self.success = True
        self.code = code
        self.data = data
        self.user_message = user_message
        self.system_message = system_message
        self.server_time = datetime.now()

    def build(self):
        return jsonify(
            {
                'code': self.code,
                'success': self.success,
                'data': self.data,
                'message': self.user_message,
                'system_message': self.system_message,
                'server_time': self.server_time,
            }
        )

    def on_success(self, data):
        self.data = data

    def on_error(self, code=200, data=None, user_message="", system_message=""):
        self.success = False
        self.code = code
        self.data = data
        self.user_message = user_message
        self.system_message = system_message
        if system_message == "":
            self.system_message = str(code)

    def on_exception(self, e):
        logger.exception(e)
        print(e)
        self.success = False

        code = 99
        message = str(e)
        description = ""
        if isinstance(e, HTTPException):
            code = e.code
        if hasattr(e, 'description'):
            description = e.description

        self.user_message = "Exception"
        self.system_message = f"Type {e.__class__.__name__}. Exception: {message}. Description: {description}"
        self.code = code

from flask import jsonify


class ServiceResponse:
    def __init__(self, code=200, data=None, message=""):
        self.code = code
        self.data = data
        self.message = message

    def on_success(self, data):
        return jsonify(
            {
                'code': 200,
                'data': data,
                'message': ''
            }
        )

    def on_error(self, message, code=200):
        return jsonify(
            {
                'code': code,
                'data': None,
                'message': message
            }
        )

    def on_exception(self, message, code=200):
        return jsonify(
            {
                'code': code,
                'data': None,
                'message': message
            }
        )

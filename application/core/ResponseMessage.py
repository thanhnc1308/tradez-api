from flask import jsonify


class ResponseMessage:
    status = 200
    data = None
    success = True
    message = None

    def __init__(self, status=200, data=None, success=True, message=None):
        self.status = status
        self.data = jsonify(data)
        self.success = success
        self.message = message

    def on_success(self, data):
        self.data = jsonify(data)
        return jsonify(ResponseMessage(self.status, self.data, self.success, self.message))

    def on_error(self, message=None):
        self.status = 400
        self.message = message
        return jsonify(ResponseMessage(self.status, self.data, self.success, self.message))

    def on_exception(self, message=None):
        self.status = 403
        self.message = 'message'
        return jsonify(ResponseMessage(self.status, self.data, self.success, self.message))
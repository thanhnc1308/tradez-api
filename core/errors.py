from werkzeug.exceptions import HTTPException


class UnauthorizedException(HTTPException):
    code = 401
    description = 'test'

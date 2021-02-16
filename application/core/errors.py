from werkzeug.exceptions import HTTPException


class DatabaseException:
    code = 500
    description = 'Database exception'

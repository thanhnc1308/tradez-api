import decimal, datetime
import json

def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def parse_sql_result(data):
    result = json.dumps([dict(row) for row in data], default=alchemy_encoder)
    return json.loads(result)
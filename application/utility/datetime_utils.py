from datetime import datetime, timedelta

def subtract_days(date, days):
    return date - timedelta(days=days)

def get_yesterday_weekday(date):
    _offsets = (3, 1, 1, 1, 1, 1, 2)
    return date - timedelta(days=_offsets[date.weekday()])

def get_the_day_before_yesterday_weekday(date):
    return get_yesterday_weekday(get_yesterday_weekday(date))

def format_date(date, format_string="%m/%d/%Y"):
    return date.strftime(format_string)

def parse_date(date_str, format_string='%d/%m/%Y'):
    return datetime.strptime(date_str, format_string)

def is_weekday(date):
    return date.weekday() < 5

from application.api.stock.Stock import Stock
from application.utility.number_utils import is_digit
from application.utility.converter import alchemy_encoder, parse_sql_result
from application.core.constants import DEFAULT_SCHEMA

dict_basic_operation = {
    'less' : ' {column} < {value} ',
    'eless' : ' {column} <= {value} ',
    'greater' : ' {column} > {value} ',
    'egreater' : ' {column} >= {value} ',
    'equal' : ' {column} = {value} ',
    'nequal' : ' {column} <> {value} ',
    'equals' : " {column} = '{value}' ",
    'like' : " {column} like '%%{value}%%' ",
    'ilike' : " {column} ilike '%%{value}%%' ",
}

dict_basic_two_operations = {
    'in_range' : ' {column} between {lower} and {upper}',
    'not_in_range' : ' {column} <= {lower} and {column} >= {upper}'
}

list_complex_operation = ['crosses', 'crosses_above', 'crosses_below']

"""[summary]
params contains:
- filters: list of filter item
- columns: list of column returned
"""
def screen_stock(params):
    data = []
    filters = params.get('filters')
    columns = params.get('columns')
    limit = params.get('limit') or 2000
    offset = params.get('offset') or 0
    sql_columns = build_sql_columns(columns)
    sql_filters = build_sql_filters(filters)
    sql = f'select {sql_columns} from {DEFAULT_SCHEMA}.stock_price where (1 = 1) {sql_filters} order by symbol offset {offset} limit {limit} ;'
    if limit == -1 and offset == -1:
        sql = f'select {sql_columns} from {DEFAULT_SCHEMA}.stock_price where (1 = 1) {sql_filters} order by symbol;'
    print(sql)
    data = Stock.execute(sql)
    return parse_sql_result(data)

def build_sql_filters(filters):
    sql = ''
    for item in filters:
        sql_filter = build_sql_filter(item)
        sql += f" and ({sql_filter}) "
    return sql

def build_sql_filter(item):
    filter_type = item.get('type')
    filter_value = parse_filter_value(item.get('value'))
    filter_operation = item.get('operation')
    if filter_operation in dict_basic_operation.keys():
        return dict_basic_operation.get(filter_operation).format(column=filter_type, value=filter_value)
    elif filter_operation in dict_basic_two_operations.keys():
        return dict_basic_two_operations.get(filter_operation).format(column=filter_type, lower=filter_value[0], upper=filter_value[1])
    elif filter_operation in list_complex_operation:
        return ''

def parse_filter_value(value):
    if is_digit(value):
        return float(value)
    elif isinstance(value, list):
        return [float(value[0]), float(value[1])]
    else:
        return f"{value}"

def build_sql_columns(columns):
    return ', '.join(columns)

def check_condition_notification(filter_list):
    res = False
    columns = []
    for filter_item in filter_list:
        columns.append(filter_item['type'])
    params = {
        'filters': filter_list,
        'columns': columns,
        'limit': -1,
        'offset': -1,
    }
    data = screen_stock(params)
    if len(data) > 0:
        res = True
    return res

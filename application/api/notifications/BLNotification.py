from application.api.notifications.Notification import Notification
from application.api.notifications.NotificationSchema import condition_schema, notification_schema, notifications_paging_schema, notifications_schema
from application.api.stock.BLStockScreener import check_condition_notification
from application.message_notification import gmail, telegram_helper
import json
from application.api.stock.crawler import crawl_all_list, crawl_all_list_at_a_date
from application.api.stock.BLStockPrice import get_indicators, get_symbols, calculate_indicators_by_list_symbol_in_a_date
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dict_basic_operation = {
    'less' : ' < ',
    'eless' : ' <= ',
    'greater' : ' > ',
    'egreater' : ' >= ',
    'equal' : ' = ',
    'nequal' : ' <> ',
    'equals' : " = ",
}

def crawl_and_send_notification():
    print('crawl_and_send_notification =========== at ', datetime.today().strftime('%Y-%m-%d'))
    try:
        date = datetime.today().strftime('%Y-%m-%d')
        # date = '2021-01-29'
        # print(date)
        print("========================crawl_data=============================")
        crawl_all_list_at_a_date(date)

        list_symbols = get_symbols('all')
        list_indicators = get_indicators('all')
        calculate_indicators_by_list_symbol_in_a_date(list_indicators, list_symbols, datetime.strptime(date, '%Y-%m-%d'))
        send_notification()
    except Exception as e:
        logger.exception(e)

def send_notification():
    all_notifications = notifications_schema.dump(Notification.get_all())
    for notification in all_notifications:
        if notification['condition_key'] != None:
            condition_key = json.loads(notification['condition_key'])
            if check_condition_notification(condition_key):
                if notification['send_gmail'] == True:
                    send_gmail(notification)
                # if notification['send_telegram'] == True:
                #     send_gmail(notification)
        break

def send_gmail(notification):
    print('send_gmail to: ', notification['gmail'])
    # if notification['gmail'] != None:
    #     gmail_message = build_notification_message(notification)
    #     gmail.send_email([notification['gmail']], gmail_message)

def build_notification_message(notification):
    arr_res = []
    condition_key = json.loads(notification['condition_key'])
    filter_symbol = ''
    filter_date = ''
    for filter_item in condition_key:
        filter_type = filter_item.get('type')
        if filter_type == 'stock_date':
            filter_date = filter_item.get('value')
        elif filter_type == 'symbol':
            filter_symbol = filter_item.get('value')
        else:
            filter_operation = get_operation_description(filter_item.get('operation'))
            filter_value = filter_item.get('value')
            filter_label = filter_item.get('label')
            filter_text = f"- {filter_label} {filter_operation} {filter_value}"
            arr_res.append(filter_text)
    arr_res.insert(0, f'Symbol {filter_symbol} at {filter_date}:')
    return '\n'.join(arr_res)

def get_operation_description(filter_operation):
    if filter_operation in dict_basic_operation:
        return dict_basic_operation.get(filter_operation)
    else:
        return filter_operation

def send_telegram(notification):
    print('send_telegram to: ', notification['tg_chat_id'])


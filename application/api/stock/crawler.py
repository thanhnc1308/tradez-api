import requests
import json
from application.api.stock.StockSchema import StockSchema
from application.api.stock.StockPrice import StockPrice
from application.api.stock.Stock import Stock

####### region Crawler
def get_stock_index(symbol):
    pass
    # url = f'https://svr4.fireant.vn/api/Data/Companies/CompanyInfo?symbol={symbol}'
    # response = requests.get(url=url)
    # if response.ok:
    #     result = json.loads(response.content)
    new_item = {
        'symbol': symbol
        # 'symbol': result.get('Symbol', None),
        # 'company_name': result.get('CompanyName', None)
    }
    Stock.create(**new_item)
    # else:
    #     print('not ok')


def get_all_stock_indices():
    url = 'https://svr4.fireant.vn/api/Data/Finance/AllLastestFinancialInfo'
    response = requests.get(url=url)
    if response.ok:
        print('ok')
        # sql = f"delete from public.stock where 1=1;"
        # Stock.execute(sql)
        data = json.loads(response.content)
        result = []
        for item in data:
            result.append(item['Symbol'])
            # get_stock_index(item['Symbol'])
        return result
    else:
        print('get_all_stock_indices not ok')

def get_crawl_url(stock_index, start_date, end_date):
    return f'https://svr1.fireant.vn/api/Data/Companies/HistoricalQuotes?symbol={stock_index}&startDate={start_date}&endDate={end_date}';

def crawl(stock_index):
    url = get_crawl_url(stock_index=stock_index, start_date='2014-07-10', end_date='2021-1-29')
    response = requests.get(url=url)
    if response.ok:
        print('ok')
        result = json.loads(response.content)
        sql = f"delete from public.stock where symbol = '{stock_index}';"
        StockPrice.execute(sql)
        for item in result:
            new_item = {
                'symbol': item.get('Symbol', None),
                'stock_date': item.get('Date', None),
                'currency_unit': 'VND',
                'open_price': item.get('PriceOpen', None),
                'high_price': item.get('PriceHigh', None),
                'low_price': item.get('PriceLow', None),
                'close_price': item.get('PriceClose', None),
                'volume': item.get('Volume', None),
                'market_cap': item.get('MarketCap', None)
            }
            StockPrice.create(**new_item)
    else:
        print('not ok')

def crawl_all_list():
    # list_stock = Stock.get_all()
    list_stock = get_all_stock_indices()
    result = []
    list_stock.sort()
    for item in list_stock:
        result.append(item)
        crawl(item)
    return result

####### endregion Crawler

####### region insert all to table

####### endregion insert all to table

####### endregion calculate and insert ema200, sma200, ema50, ema20, rsi14, macd to table stock

####### endregion event observer schedualing crawl and insert ema, rsi to table stock

####### endregion backtest: entry when, exit when, stop loss when

####### endregion pip or % calculator

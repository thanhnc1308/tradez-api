import schedule
import time
import requests
TICKER_API_URL = 'https://api.binance.com/api/v3/ticker/price?symbol='


def get_current_price(symbol):
    r = requests.get(TICKER_API_URL + symbol)
    print(float(r.json()['price']))
    return float(r.json()['price'])


# try:
#     print(get_current_price('BTCUSDT'))
# except Exception as ex:
#     print(ex)


# before_close = ":55"
# after_close = ":02"
# schedule.every().hour.at(before_close).do(get_current_price)
# schedule.every().hour.at(after_close).do(get_current_price)

schedule.every().day.at("22:21").do(get_current_price, symbol='BTCUSDT')

# Loop so that the scheduling task
# keeps on running all time.
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)

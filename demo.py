from business.crawler import crawl


data = crawl('BTC-USD', 'yahoo', '2019-1-1', '2019-12-31', 'btc-usd.csv')
print(data)

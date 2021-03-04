import sys
sys.path.append('/home/thanhnc/GR/trading-system')
from application.business.crawler import crawl
from application.business.indicators.utils import dropna
from application.business.indicators.volume import OnBalanceVolumeIndicator, MFIIndicator

df = crawl('BTC-USD', 'yahoo', '2020-1-1', '2020-08-03', 'btc-usd.csv')

# Clean nan values
df = dropna(df)

df["obv"] = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume'], fillna=True).on_balance_volume()

df["mfi"] = MFIIndicator(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume'], window=14, fillna=True).money_flow_index()

print(df.head(5))
print(df.columns)

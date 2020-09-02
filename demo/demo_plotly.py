from plotly.offline import plot
import plotly.graph_objs as go
from business.crawler import crawl
from business.indicators import ema
from business.price_action import single_candle, double_candle, triple_candle, heikin_ashi
from business.visualization import plotly

data = crawl('BTC-USD', 'yahoo', '2020-1-1', '2020-08-03', 'btc-usd.csv')
# print(data.to_string())

fig = plotly.create_figure(data)
# set some basic information
fig.update_layout(
    title='The BTC-USD Chart',
    yaxis_title='Price in $'
)
plotly.show_candlestick_patterns(fig=fig, df=data, filter_fn=single_candle.is_doji)

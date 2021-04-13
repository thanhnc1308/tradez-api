from datetime import datetime
from application.api.backtest.strategies import *


CONFIG = {
    'mode': 'backtest', # 'backtest', 'optimization', 'walk_forward', 'paper', 'live'
    'plot': True,
    'init_date': datetime(2016, 1, 1),
    'end_date': datetime(2021, 4, 10),
    'asset': 'BTC-USD',
    'capital_base': 100000.0,
    'size': 2,
    'log': False,
    'take_profit': {
        'enabled': False,
        'value': 0.01,
    },
    'stop_loss': {
        'enabled': False,
        'value': 0.02,
    },
    'strategies': [ # One or more strategies to run
        # RSIStrategy
        BollingerBandsStrategy
    ],
}

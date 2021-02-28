from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from application.api.base.BaseModel import BaseModel


class StockPrice(BaseModel):
    __tablename__ = "stock_price"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    stock_date = db.Column(db.Date, nullable=False)
    currency_unit = db.Column(db.String(10), nullable=True)
    open_price = db.Column(db.Numeric, nullable=True)
    high_price = db.Column(db.Numeric, nullable=True)
    low_price = db.Column(db.Numeric, nullable=True)
    close_price = db.Column(db.Numeric, nullable=True)
    volume = db.Column(db.Numeric, nullable=True)
    market_cap = db.Column(db.Numeric, nullable=True)
    ema200 = db.Column(db.Numeric, nullable=True)
    ema100 = db.Column(db.Numeric, nullable=True)
    ema89 = db.Column(db.Numeric, nullable=True)
    ema50 = db.Column(db.Numeric, nullable=True)
    ema34 = db.Column(db.Numeric, nullable=True)
    ema20 = db.Column(db.Numeric, nullable=True)
    sma200 = db.Column(db.Numeric, nullable=True)
    sma100 = db.Column(db.Numeric, nullable=True)
    sma50 = db.Column(db.Numeric, nullable=True)
    sma20 = db.Column(db.Numeric, nullable=True)
    rsi14 = db.Column(db.Numeric, nullable=True)
    rvi10 = db.Column(db.Numeric, nullable=True)
    obv = db.Column(db.Numeric, nullable=True)
    rsi7 = db.Column(db.Numeric, nullable=True)
    mfi14 = db.Column(db.Numeric, nullable=True)
    atr14 = db.Column(db.Numeric, nullable=True)
    adx14 = db.Column(db.Numeric, nullable=True)
    cci20 = db.Column(db.Numeric, nullable=True)
    cmf20 = db.Column(db.Numeric, nullable=True)
    mfi14 = db.Column(db.Numeric, nullable=True)
    macd_level_12_26 = db.Column(db.Numeric, nullable=True)
    macd_signal_12_26 = db.Column(db.Numeric, nullable=True)
    bb_20_lower = db.Column(db.Numeric, nullable=True)
    bb_20_upper = db.Column(db.Numeric, nullable=True)
    williams_percent_range_14 = db.Column(db.Numeric, nullable=True)
    awesome_oscillator = db.Column(db.Numeric, nullable=True)
    stochastic_k_14_3_3 = db.Column(db.Numeric, nullable=True)
    stochastic_d_14_3_3 = db.Column(db.Numeric, nullable=True)
    chaikin_money_flow_20 = db.Column(db.Numeric, nullable=True)
    parabolic_sar = db.Column(db.Numeric, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return "<Stock %s>" % self.index

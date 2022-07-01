import backtrader as bt
from backtrader.indicators import ExponentialMovingAverage as EMA

class EMAPercentDIfferenceIndicator(bt.Indicator):
    lines = ('percent_difference', 'ema')
    params = (('period', 15),)

    def __init__(self):
        # self.ema = bt.indicators.EMA(self.data, period=self.params.period)
        self.addminperiod(self.p.period)
        ema = EMA(self.data, period=self.p.period)
        self.percent_difference = (ema - self.data) / ((ema + self.data) / 2)

import backtrader as bt


class AroonStrat(bt.Strategy):
    params = (('period', 14), ('upperband', 70), ('lowerband', 30))

    def __init__(self):
        self.aroon = bt.indicators.AroonOscillator(period=self.p.period, upperband=self.p.upperband,
                                                   lowerband=self.p.lowerband)
        self.addminperiod(self.p.period)

    def next(self):
        pass

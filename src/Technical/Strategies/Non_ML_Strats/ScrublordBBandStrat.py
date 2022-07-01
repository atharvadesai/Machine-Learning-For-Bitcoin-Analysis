"""
This file contains a strategy that is similar to BBandStrat that doesn't use machine learning.
The purpose is to compare its results to the ML results
"""
import backtrader as bt


class BBandStratForNonMLScrubs(bt.Strategy):
    """
    This strategy is like the one found here
    https://backtest-rookies.com/2018/02/23/backtrader-bollinger-mean-reversion-strategy/
    It is only used for testing purposes to compare the gains made by an ML strategy to a non ML strategy
    Entry Conditions:
        Long:
            - Price closes below bot band
            - Stop Order for when price crosses back above the bot band

        Short:
            - Price closes above top band
            - Stop Order for when price crosses back below top band

    Exit: when price touches the middle line or predicts the price touching the middle line

    Parameters:
    size: The number of shares to use in a trade
    """

    params = (('trade_amount', 10), ('trade_size', 10), ('trade_fractions', False), ('period', 20), ('devfactor', 2), ('movav', bt.indicators.MovingAverageSimple))

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor, movav=self.p.movav)

    def next(self):

        # Cancel any orders which have been put in but not executed yet
        [self.broker.cancel(order) for order in self.broker.get_orders_open()]
        if not self.position:
            if self.data.close[0] > self.bbands.top[0]:
                # The next tick's price is predicted to go above the top band
                # Got Short
                if self.p.trade_fractions:
                    self.order_target_value(target=-self.p.trade_amount, price=self.bbands.top[0])
                else:
                    self.sell(exectype=bt.Order.Stop, price=self.bbands.top[0], size=self.p.trade_size)
            if self.data.close[0] < self.bbands.bot[0]:
                # The next tick's is predicted to go below the bot band
                # Go Long
                if self.p.trade_fractions:
                    self.order_target_value(target=self.p.trade_amount, price=self.bbands.bot[0])
                else:
                    self.buy(exectype=bt.Order.Stop, price=self.bbands.bot[0], size=self.p.trade_size)
        else:
            # Currently in a position
            if self.position.size > 0:
                # Currently going Long
                if self.p.trade_fractions:
                    self.sell(exectype=bt.Order.Limit, price=self.bbands.mid[0], size=self.position.size)
                else:
                    self.sell(exectype=bt.Order.Limit, price=self.bbands.mid[0], size=self.p.trade_size)
            else:
                # Currently going Short
                if self.p.trade_fractions:
                    self.buy(exectype=bt.Order.Limit, price=self.bbands.mid[0], size=-self.position.size)
                else:
                    self.buy(exectype=bt.Order.Limit, price=self.bbands.mid[0], size=self.p.trade_size)

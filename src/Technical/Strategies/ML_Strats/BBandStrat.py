import backtrader as bt
from util import formatData


class BBandStrat(bt.Strategy):
    """
    Entry Conditions:
        Long:
            - Predictor predicts the price closing below the lower band

        Short:
            - Predictor predicts the price closing above the upper band

    Exit: when price touches the middle line or predicts the price touching the middle line



    Parameters:
    trade_fractions: If True, will trade $trade amount at a time, if False (default) will trade size shares at a time
    trade_amount: The amount to buy at a time in dollars
    trade_size: The number of shares to use in a trade
    BBrand Parameters: period, devfactor, movav
    BBand_predictors: dict with SKLearn models as values for the BBand lines
    BBand_predictor_period is the number of ticks to use as inputs for the SKLearn models
    BarPredictor: Technical.util.BarPredictor (Predicts all values for the next bar)
    """


    params = (('trade_amount', 10), ('trade_size', 10), ('trade_fractions', False),
              ('period', 20), ('devfactor', 2), ('movav', bt.indicators.MovingAverageSimple),
              ('BBand_predictors', {'top': None, 'mid': None, 'bot': None}), ('BBand_predictor_period', None),
              ('Bar_predictor', None), ('data_log', {}))

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor, movav=self.p.movav)
        self.predictors = self.p.BBand_predictors
        self.pred_period = self.p.BBand_predictor_period
        self.bar_predictor = self.p.Bar_predictor
        self.min_bar = max(self.p.period, self.p.BBand_predictor_period) + self.bar_predictor.input_length
        self.p.data_log['ptop'] = []
        self.p.data_log['pmid'] = []
        self.p.data_log['pbot'] = []
        self.p.data_log['pclose'] = []
        self.p.data_log['top'] = []
        self.p.data_log['mid'] = []
        self.p.data_log['bot'] = []
        self.p.data_log['close'] = []

    def next(self):
        if len(self.data) < self.min_bar:
            return


        predictions = {'top': self.predictors['top'].predict(formatData(self.bbands.top, self.pred_period))[0],
                       'mid': self.predictors['mid'].predict(formatData(self.bbands.mid, self.pred_period))[0],
                       'bot': self.predictors['bot'].predict(formatData(self.bbands.bot, self.pred_period))[0]}
        tommorow = self.bar_predictor.predict(self.data)
        self.p.data_log['ptop'].append(predictions['top'])
        self.p.data_log['pmid'].append(predictions['mid'])
        self.p.data_log['pbot'].append(predictions['bot'])
        self.p.data_log['pclose'].append(tommorow['close'])
        self.p.data_log['top'].append(self.bbands.top[0])
        self.p.data_log['mid'].append(self.bbands.mid[0])
        self.p.data_log['bot'].append(self.bbands.bot[0])
        self.p.data_log['close'].append(self.data.close[0])
        # Cancel any orders which have been put in but not executed yet
        [self.broker.cancel(order) for order in self.broker.get_orders_open()]
        if not self.position:
            if tommorow['close'] > predictions['top']:
                # The next tick's price is predicted to go above the top band
                # Got Short
                if self.p.trade_fractions:
                    # self.order_target_value(target=-self.p.trade_amount)
                    # Set price to the average of the prediction and now
                    b, p = self.bbands.bot[0], predictions['top']
                    price = (b + p) / 2
                    self.order_target_value(target=-self.p.trade_amount, price=price)
                else:
                    self.sell(size=self.p.trade_size)
            if tommorow['close'] < predictions['bot']:
                # The next tick's is predicted to go below the bot band
                # Go Long
                if self.p.trade_fractions:
                    # self.order_target_value(target=self.p.trade_amount)
                    # Set price to the average of the prediction and now
                    b, p = self.bbands.bot[0], predictions['bot']
                    price = (b + p) / 2
                    self.order_target_value(target=self.p.trade_amount, price=price)
                else:
                    self.buy(size=self.p.trade_size)
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

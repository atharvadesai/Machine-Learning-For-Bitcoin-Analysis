from Technical.util import getDataFrame, TrainModels, formatData
from sklearn.linear_model import BayesianRidge


class BarPredictor(object):
    """
        This class contains predictors for attempting to predict all values for the next
    bar (Open,High,Low,Close,Adj Close,Volume)
    """

    def __init__(self, train_range: tuple, input_length: int, output_offset=1, save_memory=False):
        """

        :param train_range: tuple (datetime, datetime)
        :param input_length: Number of inputs to train on
        :param output_offset: How many bars into the future that you want to predict (Must be a positive integer)
        :param save_memory: If True, will train predictors one at a time. Use if you don't have enough ram or
            dataset is very large.
        """
        self.train_range = train_range
        self.input_length = input_length
        self.output_offset = output_offset

        self.predictors = {'open': BayesianRidge(), 'high': BayesianRidge(), 'low': BayesianRidge(),
                           'close': BayesianRidge(), 'adj_close': BayesianRidge(), 'volume': BayesianRidge()}
        data = getDataFrame(train_range[0], train_range[1]).drop(columns=['Date'])
        predictors = [self.predictors['open'], self.predictors['high'], self.predictors['low'],
                      self.predictors['close'], self.predictors['adj_close'], self.predictors['volume']]

        TrainModels(predictors, data, self.input_length, save_memory, self.output_offset)
        self.data = None

    def predict(self, datas):
        self.data = datas
        return dict(open=self.open, high=self.high, low=self.low, close=self.close, adj_close=self.adj_close,
                    volume=self.volume)

    @property
    def open(self):
        if self.data is None:
            return 0
        else:
            return self.predictors['open'].predict(formatData(self.data.open, self.input_length))[0]

    @property
    def high(self):
        if self.data is None:
            return 0
        else:
            return self.predictors['high'].predict(formatData(self.data.open, self.input_length))[0]

    @property
    def low(self):
        if self.data is None:
            return 0
        else:
            return self.predictors['low'].predict(formatData(self.data.open, self.input_length))[0]

    @property
    def close(self):
        if self.data is None:
            return 0
        else:
            return self.predictors['close'].predict(formatData(self.data.open, self.input_length))[0]

    @property
    def adj_close(self):
        if self.data is None:
            return 0
        else:
            return self.predictors['adj_close'].predict(formatData(self.data.open, self.input_length))[0]

    @property
    def volume(self):
        if self.data is None:
            return 0
        else:
            return self.predictors['volume'].predict(formatData(self.data.open, self.input_length))[0]

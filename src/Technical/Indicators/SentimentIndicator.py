import backtrader as bt
from random import randint


class SentimentIndicator(bt.Indicator):
    """
    sentiment line: Has a values in [0, 1]
    Parameters:
        sentiment_function: A function that takes in the current date and returns the sentiment
    """
    lines = ('sentiment',)
    params = (('predictions', []),)

    def __init__(self):
        self.sentiment = self.p.predictions

    #
    # def next(self):
    #     self.sentiment[0] = self.sent_func(self.datas[0].datetime.date(0))

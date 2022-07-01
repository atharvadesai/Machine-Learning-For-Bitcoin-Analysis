import backtrader as bt
from random import randint
import numpy as np
from random import randint
class RandomSentimentStrat(bt.Strategy):
    """
    This is a simple strategy to test the Sentiment Analysis.

    Entry:
        Long: When the sentiment analysis says that the value of bitcoin will go up
        Short: When the sentiment analysi says that the value of bitcoin will go down
    Exit:
        1 Week after entering a position.
    Parameters
    Sentiment Predictor
    trade period
    """
    params = (('trade_period', 7),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("{0}, {1}".format(dt.isoformat(), txt))

    def __init__(self):
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.entryprice = None
        self.entrycomm = None
        self.current_sentiment = 0
        self.position_entry = None

    def next(self):
        if self.order:
            # Order is currently pending.
            return
        sentiment = [-1, 1][randint(0, 1)]
        if self.position_entry is None:
            # Currently not in a position
            self.current_sentiment = sentiment
            if sentiment > 0:
                # Good sentiment, go long
                self.log("BUY CREATE ${:.2f}".format(self.data.close[0]))
                self.order = self.buy()
            else:
                # sentiment = 0, bad sentiment. Go short
                self.log('SELL CREATE ${:.2f}'.format(self.data.close[0]))
                self.order = self.sell()
            self.position_entry = len(self)


        else:
            if len(self) - self.position_entry >= self.p.trade_period:
                """
                Time to evaluate the position. 
                If the sentiment is unchanged and has shown to be correct since entering 
                position, increase the size of the bet.
                If the sentiment has changed and enter a new position.
                If the sentiment is unchanged, and the previous sentiment was shown to be incorrect, exit
                the position
                """
                sentiment_was_correct = (self.current_sentiment > 0 and  self.data.close[0] > self.entryprice) or (self.current_sentiment < 0 and self.data.close[0] < self.entryprice)
                # Time to evaluate position, first check if the sentiment has changed.
                # If it has not changed, increase bet
                if sentiment == self.current_sentiment:
                    # Sentiment is unchanged
                    log_str = "Sentiment unchanged; "
                    if sentiment_was_correct:
                        # Previous sentiment analysis has shown to be correct
                        # increase bet
                        log_str += "Previous sentiment correct; Increasing "

                        if sentiment > 0:
                            log_str += "Long Position\nBUY CREATE {:.2f}".format(self.data.close[0])
                            self.log(log_str)
                            self.log("BUY CREATE {:.2f}".format(self.data.close[0]))
                            self.order = self.buy()
                        else:
                            log_str += "Short Position\nSELL CREATE {:.2f}".format(self.data.close[0])
                            self.log(log_str)
                            self.order = self.sell()

                        self.position_entry = len(self)

                    else:
                        # Previous sentiment analysis has shown to be incorrect
                        # Exit position
                        log_str += "Previous sentiment incorrect; Exiting Position;\n {0} CREATE ${1:.2f}"\
                            .format("BUY" if self.position.size > 0 else "SELL", self.data.close[0])
                        self.log(log_str)
                        self.order = self.order_target_size(target=0)
                        self.position_entry = None

                else:
                    # Sentiment has changed
                    self.current_sentiment = sentiment
                    log_str = "Sentiment Changed; Previous sentiment "
                    # Check if sentiment was correct
                    if sentiment_was_correct:
                        log_str += "correct; Reversing Position;\n {0} CREATE ${1:.2f}"\
                            .format("BUY" if self.position.size > 0 else "SELL", self.data.close[0])
                        self.order = self.order_target_size(target=self.position.size * -1)
                        self.position_entry = len(self)
                    else:
                        log_str += "incorrect; Exiting Position;\n {0} CREATE {1:.2f}"\
                            .format("BUY" if self.position.size > 0 else "SELL", self.data.close[0])
                        self.order = self.order_target_size(target=0)
                        self.position_entry = None


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        elif order.status == order.Completed:
            self.log("{0} Executed, Price ${1:.2f}, Cost: ${2:.2f}, Commission: ${3:.2f}".format(
                "Buy" if order.isbuy() else "Sell",
                order.executed.price, order.executed.value, order.executed.comm).replace("Cost: $-", "Cost: $"))
        self.order = None

        self.entryprice = order.executed.price
        self.entrycomm = order.executed.comm


    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log("Trade Completed: GROSS {0:.2f}, NET {1:.2f}".format(trade.pnl, trade.pnlcomm))
        self.position_entry = None
    def start(self):
        print("Starting Portfolio Value: ${:.2f}".format(self.broker.getvalue()))
        self.log("Begin trading")
    def stop(self):
        self.log("End of trading")
        print("Final Portfolio Value: ${:.2f}".format(self.broker.getvalue()))


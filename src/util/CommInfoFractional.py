"""
This is necessary for trading fractional shares, as one would do with bitcoin
"""
import backtrader as bt


class CommInfoFractional(bt.CommissionInfo):
    # def getvaluesize(self, size, price):
    #     """
    #     :return: The value of size for a given price
    #     """
    #     return self.p.leverage * (size / price)
    def getsize(self, price, cash):
        # Returns fractional sizes for cash operation
        return self.p.leverage * (cash / price)

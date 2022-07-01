import unittest
import backtrader as bt
import pandas as pd
from util.IndicatorExtractor import ExtractIndicatorData
from datetime import datetime
import os


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = os.path.abspath("Test_IndicatorExtraction_Results.csv")
        self.data = bt.feeds.YahooFinanceData(dataname="BTC-USD", fromdate=datetime(2019, 1, 1),
                                              todate=datetime(2020, 1, 1))
        self.indicator_creator = lambda: lambda: [bt.indicators.ExponentialMovingAverage(self.data),
                                                  bt.indicators.MACD(self.data)]

    # def tearDown(self) -> None:
    #     del self.filename, self.data, self.indicator_creator

    # self.ema = bt.indicators.ExponentialMovingAverage(self.data)
    # self.macd = bt.indicators.MACD(self.data)

    def test_file_creation(self):
        # Plan is to iterate through data to create a .csv file, then test that that data can be made into a pandas
        # dataframe

        if os.path.isfile(self.filename):
            # Delete file if it exists
            os.remove(self.filename)
        ExtractIndicatorData(self.data, indicator_initializers=self.indicator_creator, filename=self.filename)
        self.assertTrue(os.path.isfile(self.filename))

    def test_file_readability(self):
        if not os.path.isfile(self.filename):
            ExtractIndicatorData(self.data, indicator_initializers=self.indicator_creator, filename=self.filename)
        self.assertTrue(os.path.isfile(self.filename))
        dataframe = pd.read_csv(self.filename)
        # If the file is not readable, an exception will be thrown
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

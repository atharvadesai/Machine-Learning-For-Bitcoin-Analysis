import unittest
import os
import backtrader as bt
from datetime import datetime
import yfinance as yf
from Technical.util.GetData import getDataFrame
from sklearn.linear_model import BayesianRidge
from Technical.util.ModelTrainer import TrainModels
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        train_from = datetime(2014, 1, 1)
        train_to = datetime(2019, 6, 6)
        self.train_range = (train_from, train_to)
        validation_from = datetime(2019, 6, 6)
        validation_to = datetime(2021, 6, 20)
        self.validation_range = (validation_from, validation_to)
        # self.train_file = os.path.abspath("../DataClean/BTC {0} - {1}".format(train_from, train_to))
        # validation_file = os.path.abspath("../DataClean/BTC {0} - {1}".format(validation_from, validation_to))

    def test_closing_price_prediction_accuracy(self):
        train_data = getDataFrame(self.train_range[0], self.train_range[1])
        validation_data = getDataFrame(self.validation_range[0], self.validation_range[1])
        model = BayesianRidge()
        TrainModels([model], train_data["Close"], 15)











if __name__ == '__main__':
    unittest.main()

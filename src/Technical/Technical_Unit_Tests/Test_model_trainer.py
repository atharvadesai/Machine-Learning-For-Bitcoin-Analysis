import unittest
import backtrader as bt
import os
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import BayesianRidge
from Technical.util.ModelTrainer import TrainModels
from Technical.util.IndicatorExtractor import ExtractIndicatorData


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        filename = os.path.abspath("ModelTraining_Test.csv")
        if not os.path.isfile(filename):
            data = bt.feeds.YahooFinanceData(dataname="BTC-USD", fromdate=datetime(2000, 1, 1),
                                             todate=datetime(2020, 1, 1))
            indicator_creator = lambda: lambda: [bt.indicators.ExponentialMovingAverage(data), bt.indicators.MACD(data)]
            ExtractIndicatorData(data, indicator_creator, filename, column_names="EMA,MACD,MACD Signal")
        self.dataframe = pd.read_csv(filename)

    def test_fitted(self):
        # Tests to see if the models are fitted by testing their prediction abilities on random data.
        # If the models are not fitted (TrainModels messed up) a NotFittedError will be raised
        input_length = 15
        models = [BayesianRidge()] * len(self.dataframe.columns)
        TrainModels(models, self.dataframe, input_length)
        for m in models:
            self.assertTrue(not np.isnan(m.predict([np.random.rand(input_length)])[0]))
    


if __name__ == '__main__':
    unittest.main()

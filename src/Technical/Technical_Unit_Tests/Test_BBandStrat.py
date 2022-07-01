import unittest
# import pyfolio as pf
import numpy as np
from Technical.Indicators.IndicatorPredictorTrainer import train_BBand_predictors
from Technical.Strategies.ML_Strats.BBandStrat import *
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import r2_score
from util import getData, BarPredictor, CommInfoFractional
from datetime import datetime
import pandas as pd
import os
while not os.getcwd().endswith("src"):
    os.chdir("../")

def format_data_log(data_log):
    keys = list(data_log.keys())
    keys.sort()
    predictions = [x for x in keys if x[0] == 'p']
    labels = [x for x in keys if x not in predictions]
    for l in labels:
        data_log[l] = data_log[l][1:]
    for p in predictions:
        data_log[p] = data_log[p][:-1]
    return data_log


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.indicator_creator = lambda: lambda: [bt.indicators.BollingerBands()]
        self.start_cash = 100000
        self.bband_predictor_period = None
        self.bar_predictor_period = None
        self.train_range = None
        self.validation_range = None
        self.data_interval = "1d"
        self.cerebro = None
        self.commission = 0.0025
        self.check_ml_greater_than_0 = True
        self.check_if_ml_is_better = True

        self.trade_fractions = False
        # Trade value in $
        self.trade_amount = 100
        # Number of shares per trade
        self.trade_size = 2

    def test_1(self):
        """
        Train on 2014 - 2017    Test on 2017 - 2020
        """
        self.bband_predictor_period = 25
        self.bar_predictor_period = 20
        self.train_range = (datetime(2014, 1, 1), datetime(2016, 12, 31))
        self.validation_range = (datetime(2017, 1, 1), datetime(2019, 12, 31))
        self.compare_to_NonML_Strat()

    def test_2(self):
        """
        Train on 2014 - 2016    Test on 2016 - June 2021
        """
        self.bband_predictor_period = 25
        self.bar_predictor_period = 20
        self.train_range = (datetime(2014, 1, 1), datetime(2015, 12, 31))
        self.validation_range = (datetime(2016, 1, 1), datetime(2021, 6, 20))
        self.compare_to_NonML_Strat()
        # self.run_test(bband_predictor_period, bar_predictor_period, train_range, validation_range)

    def test_3(self):
        """
        Train on 2014 - 2021    Test on 2021 - June 2021
        """
        self.bband_predictor_period = 25
        self.bar_predictor_period = 20
        self.train_range = (datetime(2014, 1, 1), datetime(2020, 12, 31))
        self.validation_range = (datetime(2021, 1, 1), datetime(2021, 6, 20))
        # self.run_test(bband_predictor_period, bar_predictor_period, train_range, validation_range)
        self.compare_to_NonML_Strat()

    def compare_to_NonML_Strat(self):
        data = getData(self.validation_range[0], self.validation_range[1], interval=self.data_interval)
        # Run ML Strat

        predictors = [BayesianRidge()] * 3  # mid, top, bot
        train_BBand_predictors(self.train_range, self.indicator_creator, predictors, self.bband_predictor_period,
                               interval=self.data_interval)
        bar_predictor = BarPredictor(self.train_range, self.bar_predictor_period)
        data_log = dict()
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.addcommissioninfo(CommInfoFractional(commission=self.commission))
        self.cerebro.adddata(data)
        self.cerebro.broker.setcash(self.start_cash)
        self.cerebro.addstrategy(BBandStrat,
                                 BBand_predictors={'mid': predictors[0], 'top': predictors[1], 'bot': predictors[2]},
                                 BBand_predictor_period=self.bband_predictor_period,
                                 Bar_predictor=bar_predictor, trade_amount=self.trade_amount, trade_size=self.trade_size,
                                 trade_fractions=self.trade_fractions, data_log=data_log)
        # self.cerebro.addanalyzer(bt.analyzers.PyFolio)
        self.cerebro.run()
        # result_ml =
        # strat_ml = result_ml[0]
        # pyfoliozer = strat_ml.analyzers.getbyname('pyfolio')
        # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
        # ts_ml = pf.create_returns_tear_sheet(returns, return_fig=True)
        # ts_ml.savefig('ts_ML.png')
        ml_profit = self.cerebro.broker.get_cash() - self.start_cash

        getmetrics(format_data_log(data_log))

        del self.cerebro

        # Run Non ML Strat
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.addcommissioninfo(CommInfoFractional(commission=self.commission))
        self.cerebro.adddata(data)
        self.cerebro.broker.setcash(self.start_cash)
        from Technical.Strategies.Non_ML_Strats.ScrublordBBandStrat import BBandStratForNonMLScrubs as NonMLStrat
        self.cerebro.addstrategy(NonMLStrat, trade_amount=self.trade_amount, trade_size=self.trade_size,
                                 trade_fractions=self.trade_fractions)
        # self.cerebro.addanalyzer(bt.analyzers.PyFolio)
        self.cerebro.run()
        # strat_no_ml = result_no_ml[0]
        # pyfoliozer = strat_no_ml.analyzers.getbyname('pyfolio')
        # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
        # ts_no_ml = pf.create_returns_tear_sheet(returns, return_fig=True)
        # ts_no_ml.savefig('ts_NO_ML.png')
        non_ml_profit = self.cerebro.broker.get_cash() - self.start_cash

        # Check Results
        strings = [
            "Train Range: {0}-{1}-{2} to {3}-{4}-{5}".format(self.train_range[0].year, self.train_range[0].month,
                                                             self.train_range[0].day,
                                                             self.train_range[1].year, self.train_range[1].month,
                                                             self.train_range[1].day, ),
            "Validation Range: {0}-{1}-{2} to {3}-{4}-{5}".format(self.validation_range[0].year,
                                                                  self.validation_range[0].month,
                                                                  self.validation_range[0].day,
                                                                  self.validation_range[1].year,
                                                                  self.validation_range[1].month,
                                                                  self.validation_range[1].day, ),
            "ML:\tProfit: ${:.2f}\tROI: {:.2f}% \nNon ML:\tProfit: ${:.2f}\tROI: {:.2f}%\n".format(
                ml_profit, ml_profit / self.start_cash * 100, non_ml_profit, non_ml_profit / self.start_cash * 100)]
        print("\n".join(strings))

        if self.check_ml_greater_than_0:
            self.assertGreaterEqual(ml_profit, 0, "${:.2f} Loss!")
        if self.check_if_ml_is_better:
            self.assertGreaterEqual(ml_profit, non_ml_profit, "Non-ML strategy was more profitable")

    # def run_test(self):
    #     # Create predictors for BBand lines
    #     predictors = [BayesianRidge()] * 3  # mid, top, bot
    #     train_BBand_predictors(self.train_range, self.indicator_creator, predictors, self.bband_predictor_period)
    #
    #     # Create predictor for each bar
    #     bar_predictor = BarPredictor(self.train_range, self.bar_predictor_period)
    #
    #     self.cerebro = bt.Cerebro()
    #
    #     data = getData(self.validation_range[0], self.validation_range[1])
    #     self.cerebro.adddata(data)
    #     self.cerebro.broker.setcash(self.start_cash)
    #     self.cerebro.addstrategy(BBandStrat,
    #                              BBand_predictors={'mid': predictors[0], 'top': predictors[1], 'bot': predictors[1]},
    #                              BBand_predictor_period=self.bband_predictor_period,
    #                              Bar_predictor=bar_predictor)
    #     self.cerebro.run()
    #
    #     end_cash = self.cerebro.broker.get_cash()
    #     profit = end_cash - self.start_cash
    #     self.assertGreaterEqual(profit, 0, "${0} Loss!".format(profit))
    #     print("Profit: ${0}\nROI {1}%\n".format(round(profit, 2), round(profit / self.start_cash * 100, 2)))
def getmetrics(data_log):
    keys = list(data_log.keys())
    preds = [x for x in keys if x[0] == 'p']
    pred_labels = [(x, x[1:]) for x in preds]
    # dfs = {x[1]: pd.DataFrame.from_dict({x[0]: data_log[x[0]], x[1]: data_log[x[1]]}) for x in pred_labels}
    for p, l in pred_labels:
        pred = np.array(data_log[p])
        label = np.array(data_log[l])
        r2 = r2_score(label, pred)
        root_mean_sqr = rmse(label, pred)
        print("{0}\nR2 Score: {1}\nRMSE: {2}".format(l, r2, root_mean_sqr))

from sklearn.metrics import mean_squared_error
def rmse(label, pred):
    # return mean_squared_error(label, pred)
    normal_label = label / np.sum(np.sqrt(label ** 2))
    normal_pred = pred / np.sum(np.sqrt(pred ** 2))
    return np.sqrt(np.average((normal_pred - normal_label) ** 2))





if __name__ == '__main__':
    unittest.main()

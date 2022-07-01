import backtrader as bt
import pandas as pd

from Technical.Strategies.ML_Strats.SimpleSentimentStrat import *
from Sentimental.SentimentPredictor import SentimentPredictor, classification_report
from util import getDataFrame, getData
from datetime import datetime
from Technical.Strategies.Non_ML_Strats.ScrublordRandomSentimentStrat import RandomSentimentStrat
import os
import pyfolio as pf
# BTC-USD data goes from 9-17-2014 to 12-31-2020
test_data_fname = 'Data/TestData.csv'

train_range = (datetime(2014, 9, 17), datetime(2020, 1, 1))
test_range = (datetime(2020, 1, 2), datetime(2020, 12, 31))
trade_period = 14
output_fname = 'Output/output.txt'
spreadsheet_fname = "Output/spreadsheet.csv"


class GenericCSV_Prediction(bt.feeds.GenericCSVData):
    lines = ('label', 'prediction')
    params = (('label', 7), ('prediction', 8), ('dtformat', "%Y-%m-%d"))


def getDataFeed():
    predictor = SentimentPredictor(train_range, test_range, trade_period)
    data_df = predictor.data
    data_df = data_df.reset_index()
    data_df['Date'] = data_df['Date'].apply(lambda x: str(x)[0:str(x).index(" ")].replace(" ", ""))
    data_df.to_csv(test_data_fname, index=False)
    data_feed = GenericCSV_Prediction(dataname=test_data_fname, fromdate=test_range[0], todate=test_range[1])
    print("Training Range: {0}\nTesting Range: {1}".format(train_range, test_range))
    return data_feed

    # prediction_feed = bt.feeds.GenericCSVData(dataname=predictor.prediction_file,
    #                                           fromdate=test_range[0], todate=test_range[1], datetime=0, prediction=1)


def run_strategy(strat, data):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    # cerebro.addanalyzer(bt.analyzers.PyFolio)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    # Normal Writer Output
    cerebro.addwriter(bt.WriterFile, out=output_fname)
    # CSV
    cerebro.addwriter(bt.WriterFile, csv=True, out=spreadsheet_fname)
    cerebro.broker.setcommission(commission=0.02)
    cerebro.broker.setcash(100000)
    cerebro.addstrategy(strat, trade_period=trade_period)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.run()
    # results = cerebro.run()

    # strat = results[0]
    # pyfoliozer = strat.analyzers.getbyname('pyfolio')
    # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    # returns = [x.to_pydatetime() for x in returns]
    # fig = pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions,
    #                                 live_start_date="{0}-{1}-{2}".format(test_range[0].year, test_range[0].month, test_range[0].day),
    #                                 round_trips=True)
    # pf.create_returns_tear_sheet(returns, positions, transactions, return_fig=True)


    cerebro.plot()


def get_classification_report():
    f = open(spreadsheet_fname, "r")
    lines = f.readlines()
    f.close()
    bounds = [i for i in range(len(lines)) if
              '===============================================================================' in lines[i]]
    lines = lines[bounds[0] + 1: bounds[1]]
    f = open(spreadsheet_fname, "w")
    f.write("\n".join(lines))
    f.close()

    # Classification report
    df = pd.read_csv(spreadsheet_fname, usecols=['label', 'prediction'])
    label, pred = df['label'], df['prediction']
    print("Classification Report:\n{0}".format(classification_report(label, pred)))


if __name__ == '__main__':
    strat = SimpleSentimentStrat
    data = getDataFeed()
    run_strategy(strat, data)
    get_classification_report()

    train_range = (datetime(2014, 9, 17), datetime(2019, 1, 1))
    test_range = (datetime(2019, 1, 2), datetime(2019, 12, 31))
    data = getDataFeed()
    run_strategy(strat, data)
    get_classification_report()
    train_range = (datetime(2014, 9, 17), datetime(2018, 1, 1))
    test_range = (datetime(2018, 1, 2), datetime(2018, 12, 31))
    data = getDataFeed()
    run_strategy(strat, data)
    get_classification_report()
    train_range = (datetime(2014, 9, 17), datetime(2017, 1, 1))
    test_range = (datetime(2017, 1, 2), datetime(2017, 12, 31))
    data = getDataFeed()
    run_strategy(strat, data)
    get_classification_report()
    train_range = (datetime(2014, 9, 17), datetime(2016, 1, 1))
    test_range = (datetime(2016, 1, 2), datetime(2016, 12, 31))
    data = getDataFeed()
    run_strategy(strat, data)
    get_classification_report()

    # Format spreadsheet file

    # cerebro.plot()

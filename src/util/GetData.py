"""
        Some simple tools that allows us to not download the same data over and over again. YahooFinance absolutely puts
    some kind of limit on how much and how often you can download data and we don't want to get put in data time out.
"""
import backtrader as bt
import os, yfinance as yf
import pandas as pd
while not os.getcwd().endswith("src"):
    os.chdir("../")
get_file_name = lambda data_name, from_date, to_date, additional_info="", interval="1d": os.path.abspath(
    "Data/{0} {3}{4} {1}to {2}.csv".format(
        data_name, from_date, to_date, additional_info + (" " if len(additional_info) > 0 else ""), interval).replace("00:00:00","").replace(":", "-"))


def getData(from_date, to_date, interval="1d", data_name="BTC-USD"):
    """
    :param from_date: datetime
    :param to_date: datetime
    :param interval: Valid Strings: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    :param data_name: Defaults to BTC-USD
    :return: Backtrader data feed
    """


    filename = get_file_name(data_name, from_date, to_date, interval=interval)
    if not os.path.isfile(filename):
        yf.download(data_name, from_date, to_date, interval=interval).to_csv(filename)

    return bt.feeds.YahooFinanceCSVData(dataname=filename, fromdate=from_date,
                                        todate=to_date, reverse=False)


def getDataFrame(from_date=None, to_date=None, interval="1d", data_name="BTC-USD", filename=None):
    """
    Like getData (see above), but returns a pandas dataframe
    Can use parameter filename if instead of other parameters
    :return: pandas DataFrame
    """
    if filename is not None:
        # This is for reading indicator data
        return pd.read_csv(filename)
    else:
        # This is for getting datafeeds as a csv file
        filename = get_file_name(data_name, from_date, to_date, interval=interval)
        if not os.path.isfile(filename):
            data = yf.download(data_name, from_date, to_date, interval=interval)
            data.to_csv(filename)
        return pd.read_csv(filename)

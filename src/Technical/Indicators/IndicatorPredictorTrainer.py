"""
This file holds a collection of methods for training predictors for different indicators
"""
import backtrader as bt

from util import getData, get_file_name, ExtractIndicatorData, getDataFrame, TrainModels


def train_BBand_predictors(train_range: tuple, indicator_creator, predictors, input_length, interval="1d", output_offset=1, save_memory=False):
    """
    :param train_range: tuple (datetime, datetime)
    :param indicator_creator: function that returns a function that returns a list of indicators
    :param predictors: list of SKLearn models to be trained
    :param input_length: The number of inputs to train the models on
    :param interval: The amount of time between bars of data (see yf.download)
    :param output_offset: See TrainModels
    :param save_memory: Set to true if you don't have enough ram to run this
    """

    train_feed = getData(train_range[0], train_range[1], interval=interval)
    BBand_file = get_file_name("BTC-USD", train_range[0], train_range[1], additional_info="BBand", interval=interval)
    ExtractIndicatorData(train_feed, indicator_creator, BBand_file, "mid,top,bot")
    train_dataframe = getDataFrame(filename=BBand_file)
    TrainModels(predictors, train_dataframe, input_length, save_memory=save_memory, output_offset=output_offset)

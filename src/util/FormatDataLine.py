import numpy as np


def formatData(data_line, length):
    """
    Formats the data to be put into a predictor
    :param data_line:  A data line from in a strategy
    :param length: How long the array needs to be
    :return: np array of the last length points on the data_line
    """
    return np.array([[data_line[-length + i] for i in range(length)]])

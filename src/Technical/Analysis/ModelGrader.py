import numpy as np
"""
This is where we will put things for grading the SKLearn models specifically
Let me know if you have any questions
- Ben
"""

def AverageSquareDistance(predictions, labels):
    """

    :param predictions: Predictions form an ml model
    :param labels: The correct value that the model is trying to predict
    :return: The average square distance from the predictions and the labels
    """
    return np.sum(np.power(predictions - labels, 2)) / labels.size

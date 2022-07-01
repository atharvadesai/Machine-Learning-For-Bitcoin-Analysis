import pandas as pd
import numpy as np
# Let me know if you have any questions
# - Ben

def TrainModels(models: list, dataframe: pd.DataFrame, input_length: int, save_memory=False, output_offset=1):
    """
 Trains multiple ml models
 :param models: List of models to train
 :param dataframe: pandas dataframe with each column being the training data for a different model
 :param input_length: The number of inputs to use as features in training
 :param output_offset: The how far into the future to predict (Must be a positive integer)
 :param save_memory: If true, will train each model one at a time to save memory, defaults to False where each model is
    trained at the same time. It will use more ram when false so make sure your computer can handle it
 :return: Nothing. The models in the list will be fitted to the input data
 """
    if save_memory:
        for i in range(len(models)):
            col = dataframe.columns[i]
            data = np.array([
                dataframe[col][index:index + input_length]
                for index in range(len(dataframe[col]) - output_offset - input_length)
            ])
            labels = np.array([
                dataframe[col][index + output_offset]
                for index in range(input_length, len(dataframe[col]) - output_offset)
            ])
            models[i].fit(data, labels)
    else:
        # Train all models at once
        datas = np.array([
            np.array([
                dataframe[col][index:index + input_length]
                for index in range(len(dataframe[col]) - output_offset - input_length)
            ])
            for col in dataframe.columns
        ])
        labels = np.array([
            np.array([
                dataframe[col][index + output_offset]
                for index in range(input_length, len(dataframe[col]) - output_offset)
            ])
            for col in dataframe.columns
        ])
        for i in range(len(models)):
            models[i].fit(datas[i], labels[i])

import pandas as pd
import numpy as np
import string

from statistics import mode

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from datetime import datetime, timedelta
from util.GetData import getDataFrame
from sklearn.metrics import accuracy_score, classification_report
import os

while not os.getcwd().endswith("src"):
    os.chdir("../")

date_to_string = lambda date: "{0}-{1}-{2}".format(date.year, date.month, date.day)


def tokenize(text):
    for x in list(string.punctuation):
        text = text.replace(x, ' ')

    for y in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        text = text.replace(str(y), '')

    text = text.lower()

    tokens = text.split()

    return tokens


class SentimentPredictor:
    def __init__(self, training_range, testing_range, period=7):
        self.training_range = training_range
        self.testing_range = testing_range
        self.period = period
        self.data = self.fetch_data()
        self.classifier = self.train_classifier()
        prediction_df = self.get_predictions()
        self.data = self.data.join(prediction_df).dropna().drop(['Headlines'], 1)

    def fetch_data(self):
        need_clean = not os.path.isfile("Sentimental/DataClean/cleaned_data.csv")
        if not need_clean:
            f = open("Sentimental/DataClean/cleaned_data.csv")
            lines = f.readlines()
            f.close()
            need_clean = len(lines) < 5

        if need_clean:
            print("Clean Headline Data not found. Need to clean dirty data.")
            from Sentimental.DataClean.clean_all_data import get_clean_data
            get_clean_data()
            print("Data has been cleaned.")

        btc_df = getDataFrame(from_date=datetime(2014, 9, 17), to_date=datetime(2020, 12, 31))
        btc_df['Label'] = np.where(btc_df['Close'].shift(-1 - self.period) - btc_df['Open'].shift(-1) > 0, 1, -1)
        btc_df['Date'] = btc_df['Date'].apply(
            lambda x: datetime(int(x.split("-")[0]), int(x.split("-")[1]), int(x.split("-")[2])))
        btc_df = btc_df.set_index('Date')


        headline_df = pd.read_csv('Sentimental/DataClean/cleaned_data.csv', index_col='Date', parse_dates=True)
        data_df = headline_df.join(btc_df, how='right')

        return data_df

    def train_classifier(self):
        tfidf = TfidfVectorizer(tokenizer=tokenize)
        model = LinearSVC()
        # data_start_date =

        # x_train = self.data['Headlines'][x_train_indicies[0]: x_train_indicies[1]]
        x_train = self.data['Headlines'].loc[self.training_range[0]: self.training_range[1] + timedelta(1)]
        x_test = self.data['Headlines'].loc[self.testing_range[0]: self.testing_range[1] + timedelta(1)]

        y_train = self.data['Label'].loc[self.training_range[0]: self.training_range[1] + timedelta(1)]
        y_test = self.data['Label'].loc[self.testing_range[0]: self.testing_range[1] + timedelta(1)]

        classifier = Pipeline([('tfidf', tfidf), ('classifier', model)])

        classifier.fit(x_train, y_train)

        print("Model Accuracy: " + str(100 * accuracy_score(y_test, classifier.predict(x_test))) + "%")

        return classifier

    def get_predictions(self):
        headlines = self.data['Headlines'].loc[self.testing_range[0]:self.testing_range[1]].loc[
                    self.testing_range[0]:self.testing_range[1]]
        # predictions = self.classifier.predict(headlines)
        prediction_df = pd.DataFrame({'Date': headlines.index, 'Prediction': self.classifier.predict(headlines)})
        prediction_df = prediction_df.set_index('Date')
        return prediction_df

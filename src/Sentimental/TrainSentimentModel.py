import yfinance as yf
import pandas as pd
import numpy as np
import string

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Fetching Bitcoin Price Data from Yahoo Finance
btc_df = yf.download('BTC-USD', period="max", interval="1d")

# Labeling Bitcoin Dataframe
btc_df['Label'] = np.where(btc_df['Close'].shift(-15) - btc_df['Open'].shift(-1) > 0, 1, -1)

# Dropping Unused Data From Bitcoin Dataframe
btc_df = btc_df.drop(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], 1)

# Fetching Preprocessed News Data
abc_df = pd.read_csv("DataClean/abc_headlines_clean.csv", index_col='Date', parse_dates=True)
cnbc_df = pd.read_csv("DataClean/cnbc_headlines_clean.csv", index_col='Date', parse_dates=True)
guardian_df = pd.read_csv("DataClean/guardian_headlines_clean.csv", index_col='Date', parse_dates=True)
reddit_df = pd.read_csv("DataClean/reddit_headlines_clean.csv", index_col='Date', parse_dates=True)
reuters_df = pd.read_csv("DataClean/reuters_headlines_clean.csv", index_col='Date', parse_dates=True)

# Create Training Dataframe
df_1 = abc_df.join(btc_df).dropna()
df_2 = cnbc_df.join(btc_df).dropna()
df_3 = guardian_df.join(btc_df).dropna()
df_4 = reddit_df.join(btc_df).dropna()
df_5 = reuters_df.join(btc_df).dropna()

training_df = df_1.append(df_2, ignore_index=True)
training_df = training_df.append(df_3, ignore_index=True)
training_df = training_df.append(df_4, ignore_index=True)
training_df = training_df.append(df_5, ignore_index=True)


def tokenize(text):

    for x in list(string.punctuation):
        text = text.replace(x, ' ')

    for y in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        text = text.replace(str(y), '')

    text = text.lower()

    tokens = text.split()

    return tokens


# Application of Supervised Learning
X = np.array(training_df['Headlines'])
Y = np.array(training_df['Label'])

tfidf = TfidfVectorizer(tokenizer=tokenize)
model = LinearSVC()

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

classifier = Pipeline([('tfidf', tfidf), ('classifier', model)])
classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)







import pandas as pd
import numpy as np
from Sentimental.DataClean.format_string import format_string

def clean_reuters_data():

    reu_df = pd.read_csv('Sentimental/DataUnclean/reuters_headlines.csv')
    reu_df = reu_df.drop(columns="Description")
    reu_df = reu_df[['Time', 'Headlines']]

    reu_df['Time'] = reu_df['Time'].apply(lambda x: correct_month(x))
    reu_df['Time'] = reu_df['Time'].apply(lambda x: reorder(x))

    for value in reu_df.Time.unique():
        concatenated_headlines = ""
        first_index = np.where(reu_df['Time'] == value)[0][0]
        last_index = np.where(reu_df['Time'] == value)[0][-1].astype(int) + 1
        for i in range(first_index, last_index):
            concatenated_headlines += format_string(reu_df['Headlines'][i])
        reu_df.loc[len(reu_df.index)] = [value, concatenated_headlines]

    reu_df = reu_df.drop(labels=range(0, 32770), axis=0)
    reu_df.rename(columns={'Time': 'Date'}, inplace=True)
    reu_df = reu_df.sort_values(by='Date')
    reu_df.to_csv('Sentimental/DataClean/reuters_headlines_clean.csv',
                  encoding='utf-8',
                  index=False)


def correct_month(x):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in months:
        if x[0:3] == month:
            if months.index(month) + 1 < 10:
                x = x.replace(x[0:3], "0" + str(months.index(month) + 1))
            else:
                x = x.replace(x[0:3], str(months.index(month) + 1))
    return x


def reorder(x):

    month = x[:2]
    day = x[3:5]
    year = x[-4:]

    return year + '-' + month + '-' + day


# clean_reuters_data()
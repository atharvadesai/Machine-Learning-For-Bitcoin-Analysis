import datetime

import pandas as pd
import numpy as np
from Sentimental.DataClean.format_string import format_string




def clean_guardian_data():

    gd_df = pd.read_csv("Sentimental/DataUnclean/guardian_headlines.csv")
    gd_df['Time'] = gd_df['Time'].apply(lambda x: format_date(x))


    for value in gd_df.Time.unique():
        concatenated_headlines = ""
        first_index = np.where(gd_df['Time'] == value)[0][0]
        last_index = np.where(gd_df['Time'] == value)[0][-1].astype(int) + 1
        for i in range(first_index, last_index):
            concatenated_headlines += " " + format_string(gd_df['Headlines'][i])
        while concatenated_headlines[0] == " ":
            concatenated_headlines = concatenated_headlines[1:]
        gd_df.loc[len(gd_df.index)] = [value, concatenated_headlines]

    gd_df = gd_df.drop(labels=range(0, 17800), axis=0)
    gd_df.rename(columns = {'Time':'Date'}, inplace = True)

    gd_df = gd_df.sort_values('Date')

    gd_df.to_csv('Sentimental/DataClean/guardian_headlines_clean.csv', index=False)
    f = open('Sentimental/DataClean/guardian_headlines_clean.csv', "r")
    lines = f.read().split("\n")
    f.close()
    lines = [lines[0]] + lines[2:]
    f = open('Sentimental/DataClean/guardian_headlines_clean.csv', "w")
    f.write("\n".join(lines))
    f.close()

month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
              'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
def format_date(x):

    if x.count("-") < 2:
        return pd.Timestamp(year=1900, month=1, day=1)
    x = x.replace(" ", "")
    day, month, year = x.split("-")
    day = int(day)
    month = int(month_dict[month])
    year = int(year) + 2000

    return pd.Timestamp(year=year, month=month, day=day)


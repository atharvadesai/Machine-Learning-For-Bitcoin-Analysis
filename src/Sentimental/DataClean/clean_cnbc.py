import os
while not os.getcwd().endswith("src"):
    os.chdir("../")

import pandas as pd
from datetime import datetime
from Sentimental.DataClean.format_string import format_string

cnbc_file = "Sentimental/DataClean/cnbc_headlines_clean.csv"
def clean_cnbc_data():
    df = pd.read_csv("Sentimental/DataUnclean/cnbc_headlines.csv")
    day_l = []
    day_headlines = {}
    month_map = {"Jan": 1, "Feb": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
                 "Aug": 8, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    for i in range(len(df)):
        if False in [isinstance(df[x][i], str) for x in ["Headlines", "Time"]]:
            continue
        hl = df["Headlines"][i]
        words = df["Time"][i].split(" ")
        year = int(words[-1])
        month = month_map[words[-2]]
        day = int(words[-3])
        date = datetime(year, month, day)
        if date in day_headlines:
            day_headlines[date] += " " + hl
        else:
            day_l.append(date)
            day_headlines[date] = hl

    new_df = pd.DataFrame({"Date": [str(x).replace(" 00:00:00", "") for x in day_l],
                           "Headlines": [format_string(day_headlines[x]) for x in day_l]})
    new_df =  new_df.sort_values(by='Date')
    new_df.to_csv(cnbc_file, index=False)





if __name__ == '__main__':
    clean_cnbc_data()
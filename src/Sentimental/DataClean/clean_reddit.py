import pandas as pd
from Sentimental.DataClean.format_string import format_string

def clean_reddit_data():

    reddit_df = pd.read_csv("Sentimental/DataUnclean/reddit_headlines.csv")
    # Drop unnecessary dates
    last_drop_row = -1
    check_date = lambda i: max(last_drop_row, i) if int(reddit_df['Date'][i].split("-")[0]) < 2014 else last_drop_row
    for row in range(len(reddit_df)):
        old_last_drop_row = last_drop_row
        last_drop_row = check_date(row)
        if last_drop_row == old_last_drop_row:
            break
    reddit_df = reddit_df[last_drop_row + 1:]

    reddit_df = concatenate_top_headlines(reddit_df)
    reddit_df = reddit_df.drop(['Label'], 1)
    reddit_df.rename(columns={'News': 'Headlines'}, inplace=True)
    reddit_df.to_csv('Sentimental/DataClean/reddit_headlines_clean.csv',
                     encoding='utf-8',
                     index=False)


def concatenate_top_headlines(dataframe):

    concatenated_headlines = []

    num_days = len(dataframe.index)

    for row in range(num_days):
        concatenated_headlines.append(' '.join(format_string(str(x))
                                               for x in
                                               dataframe.iloc[row, 2:27]))
    while concatenated_headlines[0] == " ":
        concatenated_headlines = concatenated_headlines[1:]
    dataframe['News'] = concatenated_headlines

    for num in range(1, 26):
        dataframe = dataframe.drop(['Top' + str(num)], 1)

    return dataframe


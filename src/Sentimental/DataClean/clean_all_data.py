import os
while not os.getcwd().endswith("src"):
    os.chdir("../")

import pandas as pd
from Sentimental.DataClean.clean_abc import clean_abcnews_data
from Sentimental.DataClean.clean_cnbc import clean_cnbc_data
from Sentimental.DataClean.clean_guardian import clean_guardian_data
from Sentimental.DataClean.clean_reuters import clean_reuters_data
from Sentimental.DataClean.clean_reddit import clean_reddit_data

def clean_data_sets():
    clean_abcnews_data()
    from multiprocessing import Pool, cpu_count
    pool = Pool(max(cpu_count(), 4))
    results = []
    for func in [clean_cnbc_data,
        clean_guardian_data,
        clean_reddit_data,
        clean_reuters_data]:
        results.append(pool.apply_async(func))
    pool.close()
    pool.join()
    [x.get() for x in results]



def combine_func(series1:pd.Series, series2:pd.Series):
    return series1.str.cat(series2, sep=' ')





def get_clean_data():
    clean_data_sets()
    dfs = [pd.read_csv("Sentimental/DataClean/" + x, index_col='Date', parse_dates=True) for x in
           'abc_headlines_clean.csv cnbc_headlines_clean.csv guardian_headlines_clean.csv reddit_headlines_clean.csv reuters_headlines_clean.csv'.split(
               " ")]
    # dfs.sort(key=lambda x: len(x))
    df = dfs[0]
    for next_df in dfs[1:]:
        df = df.combine(next_df, combine_func, fill_value='')
    # engine = create_engine('sqlite:///Sentimental/DataClean/clean_data.db', echo=False)
    # meta = MetaData()
    # Data = Table('Data', meta, Column('Date', DateTime, primary_key=True), Column('Headline', String()))
    # Data.create(engine)
    # meta.create_all(engine)
    # df.index = pd.to_datetime((df.index))
    # types = set()
    # df.index = df.index.map(lambda x: types.add(type(x)))
    # df.to_sql(name='Data', con=engine, if_exists='replace', index=True)
    df.to_csv("Sentimental/DataClean/cleaned_data.csv")






if __name__ == '__main__':
    get_clean_data()

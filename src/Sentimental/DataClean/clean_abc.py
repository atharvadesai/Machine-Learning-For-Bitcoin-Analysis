from datetime import datetime
from multiprocessing import Pool, cpu_count
import numpy as np
import pandas as pd
from Sentimental.DataClean.format_string import format_string
import os
while not os.getcwd().endswith("src"):
    os.chdir("../")
abc_file = "Sentimental/DataClean/abc_headlines_clean.csv"
get_datetime = lambda line: str(datetime(int(line[:4]), int(line[4:6]), int(line[6:8]))).replace(" 00:00:00", "")


# "".join([x if x.isalpha() else "" if x.isalnum() else " " for x in string]).lower()
def clean_abcnews_data():
    f = open("Sentimental/DataUnclean/abc_headlines.csv", "r")
    lines = f.read().split("\n")
    f.close()
    line_2014 = min(range(len(lines)), key=lambda i: i if lines[i].startswith("2014") else float("inf"))
    new_lines = lines[line_2014:]
    del lines
    # Get ordered list of dates without duplicates
    date_l = [get_datetime(line) for line in new_lines]
    checked_dates = set()
    dates = []
    for d in date_l:
        if d in checked_dates:
            continue
        dates.append(d)
        checked_dates.add(d)
    del date_l
    del checked_dates

    date_first_line = get_date_first_lines(dates, new_lines)
    chuncked_dates = chunk_list(dates, cpu_count())
    pool = Pool(cpu_count())
    async_results = [pool.apply_async(get_date_headlines, args=(d, date_first_line, new_lines)) for d in chuncked_dates]
    pool.close()
    pool.join()
    date_headlines = {}
    for async_res in async_results:
        new_dict = async_res.get()
        for d in new_dict:
            date_headlines[d] = new_dict[d]
    # zipped = ((d, date_headlines[d]) for d in dates)
    # Now to write the csv file
    new_f = open(abc_file, "w")
    new_f.write("")
    new_f.close()
    new_df = pd.DataFrame({"Date": [str(x).replace(" 00:00:00", "") for x in dates],
                           "Headlines": [format_string(date_headlines[x]) for x in dates]})
    new_df.to_csv(abc_file, index=False)
    #
    # new_f = open(abc_file, "a")
    # new_f.write("Date,Headlines\n")
    # for ds in chuncked_dates:
    #     string = "\n".join(["{0},{1}".format(date, date_headlines[date]) for date in ds])
    #     new_f.write(string)
    # new_f.write("\n")


    # for date in dates:
    #     new_f.write("{0},{1}\n".format(date, date_headlines[date]))
    # new_f.close()


def get_date_headlines(dates, date_first_line, lines):
    """
    :param dates: list of dates
    :param date_first_line:
    :param lines:
    :return: dict mapping dates to their concatenated headline
    """
    date_headlines = {}
    for i in range(len(dates)):
        end_line = len(lines) if i == len(dates) - 1 else date_first_line[dates[i + 1]]
        rel_lines = lines[date_first_line[dates[i]]: end_line]
        string = "".join([" " + x[9:] for x in rel_lines])
        string = "".join([x if x.isalpha() else "" if x.isalnum() else " " for x in string]).lower().replace(",", " ")
        string = string.replace("  ", " ")
        if string.startswith(" "):
            string = string[1:]
        date_headlines[dates[i]] = string
    return date_headlines


def get_date_first_lines(dates, lines):
    """
    :param dates: list of dates
    :param lines: list of lines
    :return: dict that maps the date string to the index of the first line
    """
    date_first_line = {date: np.nan for date in dates}
    date_first_line[dates[0]] = 0
    pool = Pool(cpu_count())
    first_line_results = []
    i = 0
    while i < len(dates):
        d = dates[i: max(i + cpu_count(), len(dates))]
        i += len(d)
        start_index = min(range(1, len(lines)), key=lambda x: x - 1 if get_datetime(lines[x]) == d[0] else float("inf"))
        first_line_results.append(pool.apply_async(find_first_lines, args=(d, start_index, lines)))
    pool.close()
    pool.join()
    for async_res in first_line_results:
        res_dict = async_res.get()
        for key in res_dict:
            date_first_line[key] = res_dict[key]
    return date_first_line


def find_first_lines(dates, start, lines):
    date_start = {}
    for i in range(len(dates)):
        date = dates[i]
        if len(date_start) > 0:
            start = date_start[dates[i - 1]]
        date_start[date] = find_first_line(date, start, lines)

    return date_start


def find_first_line(date, start, lines):
    for i in range(start, len(lines)):
        if get_datetime(lines[i]) == date:
            return i
    return len(lines) - 1


def chunk_list(lst, num_chunks):
    divs = list()
    chunk_length = int(len(lst) / num_chunks)
    for i in range(0, len(lst), chunk_length):
        divs.append(lst[i: i + chunk_length])
    return divs


if __name__ == '__main__':
    clean_abcnews_data()

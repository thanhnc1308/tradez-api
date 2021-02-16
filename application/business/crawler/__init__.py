import pandas as pd
from pandas_datareader import data
SRC = './business/crawler/data/'


def crawl(index, source, start_date, end_date, file_name):
    """
    function crawl data using pandas_reader
    :param index: i.e GOOG for google stock
    :param source: i.e yahoo
    :param start_date:
    :param end_date:
    :param file_name: name.csv
    :return: Pandas DataFrame
    """
    file_dir = SRC + file_name
    try:
        crawled_data = pd.read_csv(file_dir)
        print('File data found...reading data')
    except FileNotFoundError:
        print('File not found...downloading the data')
        crawled_data = data.DataReader(index, source, start_date, end_date)
        crawled_data.to_csv(file_dir)
    return crawled_data

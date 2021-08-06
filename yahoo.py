# Import the necessary modules
import pandas as pd
import yfinance as yf
import os

os.system("date")
yf.pdr_override()

def get_data(filename="file1"):
    # Get the current SP components, and get a tickers list
    file = open(filename, 'r')
    lines = file.readlines()
    stocks = []
    for line in lines:
        line = line.strip('\n')
        #parts = line.split(' ') # If multiple tickers separated by space
        parts = line.split(',') # If multiple tickers separated by comma

        stocks = stocks + parts
        #stocks.append(row)
    stocks = list(dict.fromkeys(stocks))
    # print(stocks)

    try:
        data = yf.download(stocks, period="1y", as_panel=False)
        output = '{}.pkl'.format(filename)
        data.to_pickle(output)
        print('Data saved at {}'.format(output))
    except ValueError:
        print('Failed download, try again.')
        data = None
    return data


if __name__ == '__main__':
    data = get_data(filename="file1")  # Don't give any extensions to ticker file
    # data = get_data(filename="file2")



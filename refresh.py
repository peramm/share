# Import the necessary modules
import pandas as pd
import yfinance as yf
import numpy as np 
import os
import datetime
import sys

# print("Creating personal ticker file from: index tech div and nondiv")
# os.system("cat index.txt tech.txt div.txt nondiv.txt > personal")
yf.pdr_override()
os.system("date")

def df_from_file (fname):
    
    filename = "{}.pkl".format(fname)
    try:
        df = pd.read_pickle(filename)
        return df
    except Exception:
        print("No such file ", filename)
        return pd.DataFrame()

def refresh_data(filename):
    # Get the current SP components, and get a tickers list

    df = df_from_file(filename)
    if len(df.index) == 0:
        return
    
    stocks = (df.columns.get_level_values(1)).tolist() # Get indices of stocks
    stocks = list(dict.fromkeys(stocks)) # indices to list and remove duplicates

    filterrows = 2
    lastrowindex = df.index[-filterrows]
    startdate = lastrowindex.strftime("%Y-%m-%d")
    #Download historical data to a multi-index DataFrame
    try:
        ndf = yf.download(stocks, start=startdate, end=None, as_panel=False)
        data = df[:-filterrows] #remove last row
        data = data.append(ndf) # Add new rows
        filename = filename+'.pkl'
        data.to_pickle(filename)
        print('Data saved at {}'.format(filename))
    except ValueError:
        print('Failed download, try again.')
        data = None

def portfolio_get_all():
    args = len(sys.argv)

    if args == 1:
        refresh_data(filename="ndx")

    else:
        for i in range(1,args):
            refresh_data(filename=sys.argv[i])


if __name__ == '__main__':
    portfolio_get_all()

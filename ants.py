import btalib
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

# Read a csv file into a pandas dataframe
#df = pd.read_csv('LEN.csv', parse_dates=True, index_col='Date')
# sma = btalib.atr(df, period=4)
# print(sma.df)
def isNaN(num):
    return num != num

def ants(fname):
    
    filename = "../pickle/{}.pkl".format(fname)
    try:
        df = pd.read_pickle(filename)
    except Exception:
        print("No such file ", filename)
        return
    stocks = (df.columns.get_level_values(1)).tolist() # Get indices of stocks
    stocks = list(dict.fromkeys(stocks)) # indices to list and remove duplicates

    columns = (df.columns.get_level_values(0)).tolist() # Get indices of parameters
    columns = list(dict.fromkeys(columns)) #parameters to list and remove duplicates

    el= pd.DataFrame(columns=['Stock'])

    for stock in tqdm(stocks):
        ndf = pd.DataFrame()
        for column in columns:
            ndf[column] = df[column][stock]
        ndf = ndf[~ndf.index.duplicated()] # Getting duplicated columns sometimes
        ndf.dropna(inplace=True)   

        ndf = ndf[ndf.index >= (datetime.now()-timedelta(days=365))]
        ndf['Gain'] = ndf['Adj Close'] > ndf['Adj Close'].shift()
        ndf['ants'] = ndf['Gain'].rolling(15).sum()
        ndf ['Vol Avg'] = ndf['Volume'].rolling(15).mean()
        ndf ['Gain Pct'] = (ndf['Adj Close'] - ndf['Adj Close'].shift(15))/ndf['Adj Close']
        ndf['Vol Diff'] = (ndf['Vol Avg'] - ndf['Vol Avg'].shift(15))/ndf['Vol Avg']
        rslt_df = ndf[ndf['ants'] >= 12]

        #Filter for setups in the last 5 days
        lastdate = (datetime.now()-timedelta(days=3)).date()
        rslt_df = rslt_df.loc[lastdate:]
        times = len(rslt_df.index)
        if times > 0:
            last = rslt_df.index[-1]
            lastgain = round(rslt_df.iloc[-1, rslt_df.columns.get_loc("Gain Pct")]*100, 1)
            volgain = round(rslt_df.iloc[-1, rslt_df.columns.get_loc("Vol Diff")]*100, 1)
            antdays = round(rslt_df.iloc[-1, rslt_df.columns.get_loc("ants")], 1)

            el = el.append({'Stock': stock, 
            "Days": antdays, "End": last.date(),
            "Price Gain": lastgain,  
            "Volume Gain": volgain}, ignore_index=True)
    if len(el.index) > 0:
        print(el.set_index('Stock').sort_values(by=['End'], ascending=False).to_string())
    else:
        print("No Match")

if __name__ == '__main__':
    while True:
        fname = input("Enter name of pickle file:")
        if fname == "q" or fname == "quit":
            break
        ants(fname)
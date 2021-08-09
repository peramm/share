# Import the necessary modules
import pandas as pd
import yfinance as yf

yf.pdr_override()

# Use this program to download 1y historical data for SP500, SP400, SP600 and NDX100

def get_sp_data(which="400"):
    
    assets = []
    # Get the current SP components, and get a tickers list
    if which == "500":
        sp_assets = pd.read_html(
            'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        assets = sp_assets.Symbol.tolist()
        
    elif which == "ndx":
        sp_assets = pd.read_html(
        'https://en.wikipedia.org/wiki/Nasdaq-100')[3]
        assets = sp_assets.Ticker.tolist()

    else:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_{}_companies'.format(which)
        sp_assets = pd.read_html(url)[0]
        if which == "600":
            sp_assets = pd.read_html(url)[1]
        assets = sp_assets['Ticker symbol'].tolist()

    # Save ticker list
    if which == "ndx":
        fn = "{}".format(which)
    else:
        fn = "sp{}".format(which)
    with open(fn, "w") as outfile:
        outfile.write("\n".join(assets))
    # Download historical data to a multi-index DataFrame
    try:
        data = yf.download(assets, period="1y", as_panel=False)
        if which == "ndx":
            filename = "ndx.pkl"
        else:
            filename = 'sp{}.pkl'.format(which)
        data.to_pickle(filename)
        print('Data saved at {}'.format(filename))
    except ValueError:
        print('Failed download, try again.')
        data = None
    return data


if __name__ == '__main__':
    #get_sp_data(400)
    #get_sp_data(500)
    #get_sp_data(600)
    #get_sp_data(ndx)
    while True:
        which = input("Enter ndx or 400 or 500 or 600:")
        if which == "quit" or which == "q":
            break
        sp_data = get_sp_data(which)

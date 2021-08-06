import pandas as pd
from datetime import date, datetime

# This scan finds performance since a specific date

fname = input("Enter name of pickle file:")
filename = "{}.pkl".format(fname)
df = pd.read_pickle(filename)
stocks = (df.columns.get_level_values(1)).tolist() # Get indices of stocks
stocks = list(dict.fromkeys(stocks)) # indices to list and remove duplicates

columns = (df.columns.get_level_values(0)).tolist() # Get indices of parameters
columns = list(dict.fromkeys(columns)) #parameters to list and remove duplicates

datestr = input("Enter start date m/d/Y:")
startdate = datetime.strptime(datestr, "%m/%d/%Y")
print(startdate.date())
exportList= pd.DataFrame(columns=['Stock', "Close", "Start", "Performance %"])

for stock in stocks:
    ndf = pd.DataFrame()
    for column in columns:
        ndf[column] = df[column][stock]
    ndf = ndf.loc[startdate:]
    ndf = ndf.dropna()

    end = round(ndf.iloc[-1, ndf.columns.get_loc("Adj Close")], 2)
    start = round(ndf.iloc[0, ndf.columns.get_loc("Adj Close")], 2)

    performance = round((end-start)*100/start,2)
    #ndf = ndf.tail(30) # Filter only last 30 days
    exportList = exportList.append({'Stock': stock, "Close": end,"Start": start,"Performance %": performance}, ignore_index=True)

el = (exportList.set_index('Stock').sort_values(by=['Performance %'], ascending=False))
print(el.head(10))
print(el.tail(10))

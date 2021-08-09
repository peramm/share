Use the python scripts in the following sequence:
1. yahoo.py or sp.py to download historical data and save to a pickle file. 
2. You can feed your ticker file to yahoo.py. sp.py will query wikipedia to automatically get the right tickers.
3. Feed to pickle file to any of the studies to get results for those studies.
4. Use refresh.py to update data that was originally downloaded using yahoo.py or sp.py. It will delete the last "n" rows and refresh them. Set n to 1 to refresh just the last row. For example, during the trading day it will just refresh current day's data.
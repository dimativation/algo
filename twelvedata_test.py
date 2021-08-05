import json
from twelvedata import TDClient
import os
from time import sleep

td = TDClient(apikey="c822604c71594044b6d972cf97e9dae8")

stocks = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm']
crypto = ["BTC/USD", "ETH/USD", "XRP/USD", "BNB/USD", "ADA/USD", "MATIC/USD"]

#EUR/USD, GBP/USD, XAU/USD

all_tickers = stocks + crypto

tickers_split = list()

timeframes = ["1day", "4h", "2h", "1h", "30min", "15min", "5min", "1min"]

def create_folders(tickers):
	if not os.path.exists('Data'):
		os.makedirs('Data')
	for ticker in tickers:
		ticker = ticker.upper()
		if ticker in crypto:
			directory = f'Data/{ticker[:-4]}'
		else:
			directory = f'Data/{ticker}'
		folder_check = os.path.isdir(directory)
		if folder_check == False:
			os.mkdir(directory)
create_folders(stocks + crypto)

def split_tickers():
	for i in range(0,len(all_tickers),8):
		
		st = all_tickers[i:i+8]
		
		tickers_split.append(st)
split_tickers()

print(tickers_split)


for timeframe in timeframes:
	for st in tickers_split:
		print(timeframe)
		try:
			ts = td.time_series(
			    symbol = st, 
			    interval=timeframe,
			    outputsize=5000,
			    timezone="America/New_York",
			    order="ASC"
			)
			main_pandas = ts.as_pandas()
			print(main_pandas)
			
			for ticker in st:
				print(ticker, timeframe)
				if ticker in crypto:
					main_pandas.loc[ticker].to_csv(f"Data/{ticker[:-4]}/{ticker[:-4]}_{timeframe}_new.csv")
				else:
					main_pandas.loc[ticker].to_csv(f"Data/{ticker}/{ticker}_{timeframe}_new.csv")
		except Exception as e:
			print(e)
		sleep(65)


# main_pandas.to_csv("BABA_1day.csv")





# # with open("BABA_4h.csv", "w") as f:
# 	f.write(ts.as_csv())
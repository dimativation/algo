import numpy as np
import pandas as pd
import requests
from time import time, sleep
import os


def get_prices_stocks_daily(ticker):
	ticker = ticker.upper()
	param = {'function': 'TIME_SERIES_DAILY_ADJUSTED',
	              'symbol': ticker,
	              'outputsize': 'full',
	              'apikey':'ULJ1MXXLOJ3FW17M',
	              'datatype': 'csv'
	    }

	url = "https://www.alphavantage.co/query"
	r = requests.get(url, param)
	url_content = r.content
	no_header = url_content.split(b'\r\n')[1:]
	no_header = b'\r\n'.join(no_header)
	csv_file = open(f'Data/{ticker}/{ticker}_1D.csv', 'ab')
	csv_file.write(no_header)
	csv_file.close()


def get_prices_stocks_intraday(ticker, timeframe):
	ticker = ticker.upper()
	request_function = 'TIME_SERIES_INTRADAY_EXTENDED'
	if timeframe == '1H':
		years = ['1','2']
		interval = '60min'
		months = [str(i) for i in range(1,13)]
	elif timeframe == '15m':
		years = ['1']
		interval = '15min'
		months = [str(i) for i in range(1,13)]
	elif timeframe == '5m':
		years = ['1']
		interval = '5min'
		months = [str(i) for i in range(1,7)]
	
	slices = []

	for year in years:
		for month in months:
			slices.append(f'year{year}month{month}')

	for i in range(len(slices)):

		param = {'function': request_function,
	              'symbol': ticker,
	              'interval': interval,
	              'slice': slices[i],
	              'apikey':'UVE3MAJ1FWQE81B6',
	    }

		url = "https://www.alphavantage.co/query"
		r = requests.get(url, param)
		url_content = r.content
		
		no_header = url_content.split(b'\r\n')[1:]
		no_header = b'\r\n'.join(no_header)
		print(slices[i])
		csv_file = open(f'Data/{ticker}/{ticker}_{timeframe}.csv', 'ab')
		csv_file.write(no_header)
		csv_file.close()
		sleep(10)



def get_sma20(coin):
    url = f'https://www.alphavantage.co/query?function=SMA&symbol={coin}&interval=daily&time_period=9&series_type=open&apikey=UVE3MAJ1FWQE81B6'
    r = requests.get(url)
    data = r.json()
    print(r.url)
    print(data.keys())
    all_dates = list(data['Technical Analysis: SMA'].keys())
    sma_20 = data['Technical Analysis: SMA']
#     print(sma_20)
    prices_20 = []
    i = 1
    for key in sma_20:
        if i == 3:
            break
        prices_20.append(float(sma_20[key]['SMA']))
        i += 1
        
    print(prices_20)
    return prices_20
    

def get_sma50(coin):

    url = f'https://www.alphavantage.co/query?function=SMA&symbol={coin}&interval=daily&time_period=20&series_type=open&apikey=UVE3MAJ1FWQE81B6'
    r = requests.get(url)
    data = r.json()
    print(r.url)
    print(data.keys())
    all_dates = list(data['Technical Analysis: SMA'].keys())
    sma_50 = data['Technical Analysis: SMA']
#     print(sma_20)
    prices_50 = []
    i = 1
    for key in sma_50:
        if i == 3:
            break
        prices_50.append(float(sma_50[key]['SMA']))
        i += 1
        
    print(prices_50)
    return prices_50
    
def get_rsi(coin):
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={coin}&interval=daily&time_period=14&series_type=open&apikey=UVE3MAJ1FWQE81B6"
    r = requests.get(url)
    print(r.url)
    data = r.json()
    rsi_14 = data['Technical Analysis: RSI']
    prices_rsi = []
    i = 1
    for key in rsi_14:
        if i == 3:
            break
        prices_rsi.append(float(rsi_14[key]['RSI']))
        i += 1
        
    print(prices_rsi)
    return prices_rsi

def create_folders(tickers):
	for ticker in tickers:
		ticker = ticker.upper()
		directory = f'Data/{ticker}'
		folder_check = os.path.isdir(directory)
		if folder_check == False:
			os.mkdir(directory)
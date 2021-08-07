import io

import numpy as np
import pandas as pd
import requests
from time import time, sleep
import os



def check_existing(ticker, timeframe, reversed = False):
	if reversed == False:
		file_path = f'Data/{ticker}/{ticker}_{timeframe}.csv'
	else:
		file_path = f'Data/{ticker}/{ticker}_{timeframe}_reversed.csv'


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
	df = pd.read_csv(io.StringIO(r.content.decode()))
	df.index = df['timestamp']
	df = df.drop(columns = ['timestamp'])
	df = df.iloc[::-1]
	df['coef'] = df['adjusted_close']/df['close']
	df['adj_open'] = df['coef']*df['open']
	df['adj_high'] = df['coef']*df['high']
	df['adj_low'] = df['coef'] * df['low']
	df.to_csv('Data/'+ticker+'/'+ticker + '_1D_reversed.csv')


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

def get_crypto_prices_daily(ticker):
	ticker = ticker.upper()
	param = {'function': 'DIGITAL_CURRENCY_DAILY',
	              'symbol': ticker,
	              'market': 'USD',
	              'apikey':'ULJ1MXXLOJ3FW17M',
	              'datatype': 'csv'
	    }
	url = "https://www.alphavantage.co/query"
	r = requests.get(url, param)
	url_content = r.content
	print(url_content)
	csv_file = open(f'Data/{ticker}/{ticker}_1D.csv', 'ab')
	csv_file.write(url_content)
	csv_file.close()
	df = pd.read_csv(f'Data/{ticker}/{ticker}_1D.csv')
	df = df.iloc[::-1]
	df.to_csv(f'Data/{ticker}/{ticker}_1D_reversed.csv', index = False)

def get_crypto_prices_intraday(ticker, timeframe):
	ticker = ticker.upper()
	param = {'function': 'CRYPTO_INTRADAY',
	              'symbol': ticker,
	              'market': 'USD',
	              'interval': '60min',
	              'apikey':'ULJ1MXXLOJ3FW17M',
	              'datatype': 'csv'
	    }
	url = "https://www.alphavantage.co/query?"
	r = requests.get(url, param)
	url_content = r.content
	print(url_content)
	csv_file = open(f'Data/{ticker}/{ticker}_{timeframe}.csv', 'ab')
	csv_file.write(url_content)
	csv_file.close()
	df = pd.read_csv(f'Data/{ticker}/{ticker}_{timeframe}.csv')
	df = df.iloc[::-1]
	df.to_csv(f'Data/{ticker}/{ticker}_{timeframe}_reversed.csv', index = False)


# get_crypto_prices("BTC", "60min")

def create_folders(tickers):
	if not os.path.exists('Data'):
		os.makedirs('Data')
	for ticker in tickers:
		ticker = ticker.upper()
		directory = f'Data/{ticker}'
		folder_check = os.path.isdir(directory)
		if folder_check == False:
			os.mkdir(directory)

# create_folders(['BTC'])
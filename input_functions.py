import numpy as np
import pandas as pd
import requests
from time import time, sleep
from datetime import datetime
import os



def get_prices_stocks_daily(ticker):
    
    ticker = ticker.upper()
    param = {'function': 'TIME_SERIES_DAILY_ADJUSTED',
             'symbol': ticker,
             'outputsize': 'full',
             'apikey': 'R4892R0NICTEOPHY',
             'datatype': 'csv'
             }

    url = "https://www.alphavantage.co/query"
    r = requests.get(url, param)
    url_content = r.text
    with open(f'Data/{ticker}/{ticker}_alpha.csv',"w+") as f:
        f.write(url_content)
    main_pd = pd.read_csv(f'Data/{ticker}/{ticker}_alpha.csv')
    main_pd_inverse = main_pd.iloc[::-1]
    main_pd_inverse['coef'] = main_pd_inverse['close']/main_pd_inverse['adjusted_close']
    main_pd_inverse['adj_open'] = main_pd_inverse['open']/main_pd_inverse['coef']
    main_pd_inverse['adj_high'] = main_pd_inverse['high']/main_pd_inverse['coef']
    main_pd_inverse['adj_low'] = main_pd_inverse['low']/main_pd_inverse['coef']
    main_pd_inverse.index = main_pd_inverse['timestamp']
    main_pd_inverse = main_pd_inverse.drop(columns = ['timestamp'])

    main_pd_inverse.to_csv(f"data/{ticker}/{ticker}_1D_reversed.csv")

    sleep(2)

# get_prices_stocks_daily('C')

def get_prices_stocks_intraday(ticker, timeframe):
    csv_file = ""
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
                  'apikey':'R4892R0NICTEOPHY',
        }

    	url = "https://www.alphavantage.co/query"
    	r = requests.get(url, param)
    	url_content = r.content
    	if i == 0:	
    		no_header = url_content.split(b'\r\n')
    	else:
    		no_header = url_content.split(b'\r\n')[1:]
    	no_header = b'\r\n'.join(no_header)
    	print(slices[i])
        # csv_file = no_header + csv_file
    	csv_file = open(f'Data/{ticker}/{ticker}_{timeframe}.csv', 'ab')
    	csv_file.write(no_header)
    	csv_file.close()
    	sleep(10)

    main_pd = pd.read_csv(f'Data/{ticker}/{ticker}_{timeframe}.csv')
    main_pd_inverse = main_pd.iloc[::-1]
    main_pd_inverse.set_index('time')
    main_pd_inverse.to_csv(f"data/{ticker}/{ticker}_{timeframe}_reversed.csv",index=False)

# get_prices_stocks_intraday('C','1H')
# get_prices_stocks_intraday('C','15m')
# get_prices_stocks_intraday('C','5m')


def check_data(ticker,timeframe):
    main_pd_inverse = pd.read_csv(f'Data/{ticker}/{ticker}_{timeframe}.csv')
    main_pd_inverse.set_index('time')
    main_pd_inverse = main_pd_inverse.iloc[::-1]
    main_pd_inverse.to_csv(f"data/{ticker}/{ticker}_{timeframe}_reversed.csv",index=False, sep=',')      

check_data('WMT', '1H')
check_data('WMT', '15m')
check_data('WMT', '5m')




def get_prices_crypto_daily(ticker):
    param = {
        'function': "DIGITAL_CURRENCY_DAILY",
        'symbol': ticker,
        'market': 'USD',
        'apikey': 'R4892R0NICTEOPHY',
        'datatype': 'csv',
    }
    url = "https://www.alphavantage.co/query"
    r = requests.get(url, param)
    url_content = r.text
    with open(f'Data/{ticker}/{ticker}_alpha.csv',"w+") as f:
        f.write(url_content)
    main_pd = pd.read_csv(f'Data/{ticker}/{ticker}_alpha.csv')
    main_pd_inverse = main_pd.iloc[::-1]
    main_pd_inverse.set_index('timestamp')
    main_pd_inverse.to_csv(f"data/{ticker}/{ticker}_1D_reversed.csv",index=False)

    sleep(2)

# def print_csv(ticker):
#     df = pd.read_csv(f'Data/{ticker}/{ticker}_1H.csv')
#     date = datetime.strptime(df['time'][0], '%Y-%m-%d %H:%M:%S')
#     print(date)

# print_csv('TSLA')



# def reverse_file(ticker,timeframe):
#     main_pd = pd.read_csv(f'Data/{ticker}/{ticker}_{timeframe}.csv')
#     main_pd_inverse = main_pd.iloc[::-1]
#     main_pd_inverse.set_index('time')
#     # main_pd_inverse.index = main_pd_inverse['time']
#     # main_pd_inverse = main_pd_inverse.drop(columns = ['time'])
#     main_pd_inverse.to_csv(f"data/{ticker}/{ticker}_{timeframe}_reversed.csv", index=False)  

# reverse_file('TSLA','1H')


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
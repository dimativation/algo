import input_functions


# tickers = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm']
tickers = [ 'BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'ADA', 'MATIC']
input_functions.create_folders(tickers)
timeframes = ['1H','15m','5m']

# for ticker in tickers:
# 	print(ticker)
# 	input_functions.get_prices_stocks_daily(ticker)

for ticker in tickers:
	print(ticker)
	daily = input_functions.get_crypto_prices_daily(ticker)
	for timeframe in timeframes:
		print(timeframe)
		intraday = input_functions.get_crypto_prices_intraday(ticker, timeframe)

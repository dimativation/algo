import input_functions



def check_stocks():
	tickers = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm','Amzn','PG','Luv']
	input_functions.create_folders(tickers)
	timeframes = ['1H','15m','5m']

	for ticker in tickers[12:]:
		print(ticker)
		input_functions.get_prices_stocks_daily(ticker)
		for timeframe in timeframes:
			print(timeframe)
			input_functions.get_prices_stocks_intraday(ticker, timeframe)


def check_crypto():
	tickers = ['BTC','ETH','LTC','XRP','BCH','TRX','DOGE']
	input_functions.create_folders(tickers)
	for ticker in tickers:
		print(ticker)
		input_functions.get_prices_crypto_daily(ticker)

check_crypto()



# for ticker in tickers:
# 	daily = get_prices_stocks_daily(ticker)
# 	for timeframe in timeframes:
# 		intraday = get_prices_stocks_intraday(ticker, timeframe)




# for coin in coins:
#     prices_20 = get_sma20(coin)
#     prices_50 = get_sma50(coin)
#     prices_rsi = get_rsi(coin)
#     for i in range(len(prices_20) - 1):
#         if prices_20[i] > prices_50[i]:
#             if prices[20][i + 1] < prices_50[i + 1]:
#                 print(f"{coin} bullish crossover")
#         elif prices_20[i] < prices_50[i]:
#             if prices_20[i + 1] > prices_50[i + 1]:
#                 print(f"{coin} bearish crossover")
    
#     for i in range(len(prices_rsi) - 1):
#         if (prices_rsi[i] < 30) and (prices_rsi[i + 1] > 30):
#             print(f"{coin} oversold")
#         elif (prices_rsi[i]) > 70 and (prices_rsi[i + 1] < 70):
#             print(f"{coin} overbought")
    
#     sleep(60)



from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import datetime
import os.path
import sys
import matplotlib
import pandas


class AlphaVDailyData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        # ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        # ('close', 5),
        ('volume', 6),
        ('div', 7),
        ('split', 8),
        ('openinterest', -1),
        ('reverse', False)
    )


class AlphaVHourlyData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes), 
        ('compression', 60),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),

        ('volume', 5),
        ('openinterest', -1),
    )


class MyStrategy(bt.Strategy):

	params = (
    	('myparam', 27),
    	('exitbars', 5),
	)
	def log(self, txt, dt = None):
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		self.dataclose = self.datas[0].close
		self.order = None
		# Indicators for the plotting show
		self.ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
		self.wma = bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
		self.stoch = bt.indicators.StochasticSlow(self.datas[0])
		self.macd = bt.indicators.MACDHisto(self.datas[0])
		self.rsi = bt.indicators.RSI(self.datas[0])
		# bt.indicators.SmoothedMovingAverage(rsi, period=10)
		self.atr = bt.indicators.ATR(self.datas[0]).plot = False

	def next(self):
		# self.log(f'Close: {self.dataclose[0]}')

		if self.order:
			return

		if not self.position:			

			if self.dataclose[0] < self.dataclose[-1]:
				if self.dataclose[-1] < self.dataclose[-2]:
					self.log(f"BUY signal {self.dataclose[0]}")
					self.order = self.buy()
		else:
			
			# Already in the market ... we might sell
			if len(self) >= (self.bar_executed + 5):
			
			    # SELL, SELL, SELL!!! (with all possible default parameters)
				self.log('SELL CREATE, %.2f' % self.dataclose[0])

			    # Keep track of the created order to avoid a 2nd order
				self.order = self.sell()
		

	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
			return

		if order.status in [order.Completed]:
			if order.isbuy():
				self.log(f"Buy executed {order.executed.price} ")
			elif order.issell():
				self.log(f"Sell executed {order.executed.price} ")
			self.bar_executed = len(self)
			
		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		self.order = None



if __name__ == '__main__':

	cerebro = bt.Cerebro()

	cerebro.broker.setcash(100000)

	modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
	datapath = os.path.join(modpath, 'data/AAPL/AAPL_1D_reversed.csv')

	# df = pd.read_csv('data/AAPL/AAPL_1H.csv', header = None, parse_dates = True)
	# # df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
	# # df.index = df['time']
	# # df = df.iloc[::-1]
	

	data = AlphaVHourlyData(dataname='data/AAPL/AAPL_1H.csv')
	cerebro.adddata(data)
	cerebro.addstrategy(MyStrategy)

	print(modpath, datapath)

	print(f"starting portfolio value: {cerebro.broker.getvalue()}" )

	cerebro.run()
	cerebro.plot()

	print(f"ending portfolio value: {cerebro.broker.getvalue()}" )
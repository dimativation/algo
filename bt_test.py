from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import os, sys
import datetime
import backtrader as bt
import input_functions


# Define a Custom Datafeed Class
class AlphaVDailyData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        #('close', 4),
        ('adj-close', 5),
        # ('close', 5), # just testing
        ('volume', 6),
        ('div', 7),
        ('split', 8),
        ('openinterest', -1),
    )

# sample strategy used for plotting the data
class St(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)
        self.prices = input_functions.get_rsi()

    def our_strategy(self):
        for i in range(len(self.sma)):

# test

if __name__ == '__main__':
    data = AlphaVDailyData(dataname='Data/AAPL/AAPL_1D.csv')
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(St)
    cerebro.run()
    cerebro.plot()
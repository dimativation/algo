from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import os, sys
import datetime
import backtrader as bt


# Define a Custom Datafeed Class
class AlphaVDailyData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%d-%m-%y'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        #('close', 4),
        #('adj-close', 5),
        ('close', 5), # just testing
        ('volume', 6),
        ('div', 7),
        ('split', 8),
        ('openinterest', -1),
    )

class AlphaVHourlyData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes), 
        ('compression', 60),
        ('nullvalue', float('NaN')),
        ('dtformat', '%d-%m-%y %H:%M'),
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

class AlphaV15minData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes), 
        ('compression', 15),
        ('nullvalue', float('NaN')),
        ('dtformat', '%d-%m-%y %H:%M'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        #('adj-close', 5),
        ('volume', 5),
        ('openinterest', -1),
    )

class AlphaV5minData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes), 
        ('compression', 5),
        ('nullvalue', float('NaN')),
        ('dtformat', '%d-%m-%y %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        #('adj-close', 5),
        ('volume', 5),
        ('openinterest', -1),
    )

# sample strategy used for plotting the data
class SimpleStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)
        self.macd = bt.indicators.MACD(self.data)
        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.dataclose = self.datas[0].close
        self.ma_fast = bt.indicators.SMA(period=20)
        self.ma_slow = bt.indicators.SMA(period=50)
        self.crossover = bt.ind.CrossOver(self.ma_fast, self.ma_slow)    
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RelativeStrengthIndex()

        #define log function 
    def log(self, txt, dt=None):
        #''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    # def close_signal(self):
    #     if self.crossover < 0:
    #         return True
    #     else:
    #         return False

    # def buy_signal(self):
    #     if self.crossover > 0:
    #         return True
    #     else:
    #         return False

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm   
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


    def notify_trade(self, trade):
            if not trade.isclosed:
                return
            
            self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return
        if not self.position:
            if self.crossover > 0:
                self.order = self.buy()
        else:
            if self.crossover < 0:
                self.order = self.sell()

if __name__ == '__main__':
    #data_1D = AlphaVDailyData(dataname='Data/AAPL/AAPL_1D.csv')
    data_1H = AlphaVHourlyData(dataname='Data/AAPL/AAPL_1H.csv')
    #data_15m = AlphaV15minData(dataname='Data/AAPL/AAPL_15m.csv')
    #data_15m.plotinfo.plotmaster = data0
    
    cerebro = bt.Cerebro()
    cerebro.adddata(data_1H)
    #cerebro.adddata(data_15m)
    # resample data into 4H Frames
    #cerebro.resampledata(data_15m, timeframe=bt.TimeFrame.Minutes, compression=240)
    # set initial cast to 100000
    cerebro.broker.set_cash(100000.0)
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 10)
    # set brocker commission: 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addstrategy(SimpleStrategy)
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()

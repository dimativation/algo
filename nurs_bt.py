from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import os, sys
import datetime
import numpy as np


# Define a Custom Datafeed Class
class AlphaVDailyData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 10),
        ('high', 11),
        ('low', 12),
        #('close', 4),
        #('adj-close', 5),
        ('close', 5), # just testing
        ('volume', 6),
        ('div', 7),
        ('split', 8),
        ('openinterest', -1),
        ('fromdate',datetime.datetime(2019, 1, 1)),
        ('todate', datetime.datetime(2021, 6, 30))
    )

class AlphaVHourlyData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes), 
        ('compression', 60),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M:%S'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('separator', ',')
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

# Buy and Hold 
class BuyAndHold_1(bt.Strategy):
    #define log function 
    def log(self, txt, dt=None):
        # #''' Logging function for this strategy'''
        # dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        pass

    def start(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash

    def nextstart(self):
        # Buy all the available cash
        size = int(self.broker.get_cash() / (self.datas[0].close[0] * 1.001) )
        self.buy(size=size)
        self.log('BUY CREATE, Price: %.2f. Size: %.2f' % (self.datas[0].close[0], size))
    
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
            self.log(f'Order Canceled/Margin/Rejected {order.Rejected} / {order.Margin} / {order.Canceled}')
            self.log('Order Status: %.2f' % order.status)
            self.log('Close Price @ -1: %.2f, Open Price @ 0: %.2f' %
                    (self.datas[0].close[-1], self.datas[0].open[0]))

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return       
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))


# sample strategy used for plotting the data
class SimpleStrategy(bt.Strategy):

    #define log function 
    def log(self, txt, dt=None):
        # #''' Logging function for this strategy'''
        # dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        pass

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)
        self.macd = bt.indicators.MACD(self.data)
        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.dataclose = self.datas[0].close
        self.ma_fast = bt.indicators.SMA(period=20)
        self.ma_slow = bt.indicators.SMA(period=50)
        self.ema_fast = bt.indicators.EMA(period=5)
        self.ema_slow = bt.indicators.EMA(period=10)
        self.crossover = bt.ind.CrossOver(self.ma_fast, self.ma_slow)    
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RelativeStrengthIndex()

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
            self.log(f'Order Canceled/Margin/Rejected {order.Rejected} {order.Margin} {order.Canceled}')
            self.log('Order Status: %.2f' % order.status)

        # Write down: no pending order
        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def is_positive(self):
        if self.ma_fast > self.ma_slow:
            if self.dataclose > self.ma_fast:
                return True
        elif self.ema_fast > self.ema_slow:
            return True
        return False

    def is_negative(self):
        if self.ma_fast < self.ma_slow:
            if self.dataclose < self.ma_fast:
                return True
        elif self.ema_fast < self.ema_slow:
            return True
        return False

    def next(self):
        if self.order:
            return
        if not self.position:
            if self.is_positive():
                self.order = self.buy()
            elif self.is_negative():
                self.order = self.sell()
        else:
            if self.position.size > 0:
                if self.ema_fast < self.ema_slow:
                    self.order = self.close()
            elif self.position.size < 0:
                if self.ema_fast > self.ema_slow:
                    self.order = self.close()

def prepare_testresults(strategy, ticker, timeframe, thestrats):
    ##  get values from analyzers
    thestrat = thestrats[0]
    # sharpe
    sharpe = thestrat.analyzers.mysharpe.get_analysis()['sharperatio']
    #roi
    roi_dict = thestrat.analyzers.myroi.get_analysis()
    rol_roi = thestrat.analyzers.myrollingroi.get_analysis()         
    roi_annual_average  = 100 * np.average(list(roi_dict.values()))
    roi_annual_max      = 100 * np.max(list(roi_dict.values()))
    roi_annual_min      = 100 * np.min(list(roi_dict.values()))
    roi_monthly_average = 100 * np.average(list(rol_roi.values()))
    roi_monthly_max     = 100 * np.max(list(rol_roi.values()))
    roi_monthly_min     = 100 * np.min(list(rol_roi.values()))
    #drawdown
    dd_dict = thestrat.analyzers.mydrawdown.get_analysis()
    dd_max = dd_dict.max.drawdown
    dd_maxlength = dd_dict.max.len
    #put results in dict
    results_dict = {}
    results_dict['strategy'] = strategy.__name__
    results_dict['ticker'] = ticker
    results_dict['timeframe'] = timeframe
    results_dict['roi_monthly_average'] = roi_monthly_average
    results_dict['roi_monthly_max'] = roi_monthly_max
    results_dict['roi_monthly_min'] = roi_monthly_min
    results_dict['sharpe'] = sharpe
    results_dict['dd_max'] = dd_max
    results_dict['dd_maxlength'] = dd_maxlength
    return results_dict

if __name__ == '__main__':

    strategies = [BuyAndHold_1, SimpleStrategy]

    data_1D = AlphaVDailyData(dataname='Data/AAPL/AAPL_1D_reversed.csv')
    data_1H = AlphaVHourlyData(dataname='Data/AAPL/AAPL_1H.csv')
    
    for strategy in strategies:
        cerebro = bt.Cerebro(quicknotify = True)
        cerebro.adddata(data_1D)
        # set initial cast to 100000
        cerebro.broker.set_cash(100000.0)
        # Add a FixedSize sizer according to the stake
        cerebro.addsizer(bt.sizers.PercentSizer, percents = 10)
        # set brocker commission: 0.1% ... divide by 100 to remove the %
        #cerebro.broker.setcommission(commission=0.001)
        cerebro.addstrategy(strategy)
        # Add Analyzers
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe', timeframe= bt.TimeFrame.Months)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='mydrawdown')
        cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='myroi')
        cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name='myrollingroi', timeframe= bt.TimeFrame.Months)
        # Run
        thestrats = cerebro.run()
        
        ##  get values from analyzers
        testresults_dict = prepare_testresults(strategy, 'AAPL', '1D', thestrats)
        print(testresults_dict)

        print('Sharpe Ratio: %.2f'
            %(testresults_dict['sharpe'])
            )
        print('Monthly ROI: Avg: %.0f, Max: %.0f, Min: %.0f'%(
            testresults_dict['roi_monthly_average'],
            testresults_dict['roi_monthly_max'], 
            testresults_dict['roi_monthly_min'])
            )
        print('Max DD: %.2f, Max DD Length: %.0f'%(
            testresults_dict['dd_max'], 
            testresults_dict['dd_maxlength'])
            )
        print('finish')
        #cerebro.plot()
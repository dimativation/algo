from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import os, sys
import datetime
import pandas as pd


file =  'log_output.csv'

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
        ('fromdate',datetime.datetime(2017, 1, 1)),
        ('todate', datetime.datetime(2021, 6, 30))
    )


# Define a Custom Datafeed Class
class AlphaVDailyDataCrypto(bt.feeds.GenericCSVData):
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
        #('adj-close', 5),
        ('close', 4), # just testing
        ('volume', 5),
        ('fromdate',datetime.datetime(2021, 2, 1)),
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
        ('separator', ','),
        ('fromdate',datetime.datetime(2019, 1, 1)),
        ('todate', datetime.datetime(2021, 6, 30))

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
        self.ema_fast = bt.indicators.EMA(period=10)
        self.ema_slow = bt.indicators.EMA(period=20)
        self.crossover = bt.ind.CrossOver(self.ma_fast, self.ma_slow)    
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.log_csv = pd.DataFrame(columns=['date', 'order', 'price', 'cost', 'commission', 'gross', 'net'])
    

    #define log function 
    def log(self, txt=None, dt=None, order=None, price=None, cost=None, comission=None, gross=None, net=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        if order != None:
            df2 = pd.DataFrame({
                'date': dt.isoformat(),
                'order': order,
                'price': price,
                'cost': cost,
                'comission': comission,
                'gross': gross,
                'net': net,
                }, index = [0])
            # print(df2)
            # print("-------")
            self.log_csv = self.log_csv.append(df2)
        # print (self.log_csv)


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
                # self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #     (order.executed.price,
                #     order.executed.value,
                #     order.executed.comm))
                self.log(order ='BUY', price = order.executed.price, cost = order.executed.value, comission = order.executed.comm)
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm   
            elif order.issell():
                
                # self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #     (order.executed.price,
                #     order.executed.value,
                #     order.executed.comm))
                self.log(order ='SELL', price = order.executed.price, cost = order.executed.value, comission = order.executed.comm)

                self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected {order.Rejected} {order.Margin} {order.Canceled}')

        # Write down: no pending order
        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
        self.log(order ='CLOSE', gross = trade.pnl, net = trade.pnlcomm)

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
            # elif self.is_negative():
            #     self.order = self.sell()
        else:
            if self.position.size > 0:
                if self.ema_fast < self.ema_slow:
                    self.order = self.close()
            # elif self.position.size < 0:
            #     if self.ema_fast > self.ema_slow:
            #         self.order = self.close()

    def test_output(self):
        print("ebal tvoi rot")
        # print(file)
        self.log_csv.to_csv(file, index='date')


if __name__ == '__main__':

    data_1D = AlphaVDailyData(dataname='data/AMZN/AMZN_1D_reversed.csv')
    # data_1D = AlphaVDailyDataCrypto(dataname='data/ETH/ETH_1D_reversed.csv')

    # data_1H = AlphaVHourlyData(dataname=f'data/AMZN/AMZN_1H_reversed.csv')
    # data.save_log()
    # print(data_1D)
    # data_15m = AlphaV15minData(dataname='Data/AAPL/AAPL_15m.csv')
    # data_15m.plotinfo.plotmaster = data0
    file = f'data/AMZN/AMZN_1D_reversed_log.csv'

    cerebro = bt.Cerebro()
    
    cerebro.adddata(data_1D)
    # cerebro.addwriter(bt.WriterFile, out = 'test_log.csv',  csv=True)

    #cerebro.adddata(data_15m)
    # resample data into 4H Frames
    #cerebro.resampledata(data_15m, timeframe=bt.TimeFrame.Minutes, compression=240)
    # set initial cast to 100000
    cerebro.broker.set_cash(100000.0)
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)
    # set brocker commission: 0.1% ... divide by 100 to remove the %
    # cerebro.broker.setcommission(commission=0.001)
    cerebro.addstrategy(SimpleStrategy)
    results =  cerebro.run()
    # print(len(results))
    for result in results:
        result.test_output()
    # data.save_log()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
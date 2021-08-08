import os

import backtrader as bt
import pandas as pd
import json

class TestStrategy(bt.Strategy):
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
        with open('config.json', 'r') as config_file:
            data = json.load(config_file)
        self.ticker = data['ticker']
        self.timeframe = data['timeframe']
        self.strategy = data['strategy']

    # define log function
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
            }, index=[0])
            # print(df2)
            # print("-------")
            self.log_csv = self.log_csv.append(df2)
        # print (self.log_csv)
        
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
                self.log(order='BUY', price=order.executed.price, cost=order.executed.value,
                         comission=order.executed.comm)
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():

                # self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #     (order.executed.price,
                #     order.executed.value,
                #     order.executed.comm))
                self.log(order='SELL', price=order.executed.price, cost=order.executed.value,
                         comission=order.executed.comm)

                self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected {order.Rejected} {order.Margin} {order.Canceled}')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
        self.log(order='CLOSE', gross=trade.pnl, net=trade.pnlcomm)

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
                elif self.dataclose < self.ema_slow:
                    self.order = self.close()
            # elif self.position.size < 0:
            #     if self.ema_fast > self.ema_slow:
            #         self.order = self.close()

    def test_output(self):
        if not os.path.exists('Data'):
            os.makedirs('Data')
        if not os.path.exists(f'Data/{self.ticker}'):
            os.makedirs(f'Data/{self.ticker}')
        if not os.path.exists(f'Data/{self.ticker}/{self.strategy}'):
            os.makedirs(f'Data/{self.ticker}/{self.strategy}')
        self.log_csv.to_csv(f'Data/{self.ticker}/{self.strategy}/{self.ticker}_{self.timeframe}_{self.strategy}.csv', index=False)

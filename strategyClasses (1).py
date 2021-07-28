import backtrader as bt
import pandas as pd
import json


# import configs for filepath
with open('config.json', 'r') as config_file:
    data = json.load(config_file)
print (data)


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
            # elif self.position.size < 0:
            #     if self.ema_fast > self.ema_slow:
            #         self.order = self.close()

    def test_output(self):
        # print("ebal tvoi rot")
        # print(file)
        self.log_csv.to_csv(file, index='date')


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
        self.log_csv = pd.DataFrame(columns=['date', 'order', 'price', 'cost', 'commission', 'gross', 'net'])

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
    
    def test_output(self):
    # print("ebal tvoi rot")
    # print(file)
        self.log_csv.to_csv(file, index='date')
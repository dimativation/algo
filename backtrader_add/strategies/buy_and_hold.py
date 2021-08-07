import backtrader as bt
import pandas as pd
import json


class BuyAndHold_1(bt.Strategy):
    
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
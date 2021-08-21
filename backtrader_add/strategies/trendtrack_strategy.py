# main idea of the strategy:
# 1) identify trend
#    https://tradersbulletin.co.uk/best-indicator-to-identify-trend/
# 2) identify entry point using support and resistance
#   not implemented yet
# 3) set target and stop loss using atr
#   simple: on uptrend:     stop = price - 1*atr, target = price + 2*atr
#           on downtrend:   stop = price - 1*atr, target = price + 2*atr


import backtrader as bt
import pandas as pd
import json

class SimpleTrendTrackingStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.ma_200 = bt.indicators.SMA(period=200)
        self.ma_30  = bt.indicators.SMA(period=30)
        self.ma_15  = bt.indicators.SMA(period=15)
        self.atr = bt.ind.ATR(period=14)
        self.atrdist_stop = -1
        self.atrdist_target = 2
        self.isuptrend = False
        self.isdowntrend = False
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.pstop = None
        self.ptarget = None
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
        #print('%s, %s' % (dt.isoformat(), txt))
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
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Target: %.2f, Stop: %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm,
                    self.ptarget,
                    self.pstop))
                self.log(order='BUY', price=order.executed.price, cost=order.executed.value,
                         comission=order.executed.comm)
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():

                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))
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


    def check_if_uptrend(self):
        if (self.dataclose > self.ma_200) and (self.ma_15 > self.ma_30):
            return True
        else:
            return False

    def check_if_downtrend(self):
        if (self.dataclose < self.ma_200) and (self.ma_15 < self.ma_30):
            return True
        else: 
            return False

    def next(self):
        if self.order:
            return
        if not self.position:
            if self.check_if_uptrend():
                self.order = self.buy()
                self.isuptrend = True
                self.isdowntrend = False
                pdist_stop = self.atr[0] * self.atrdist_stop
                pdist_targ = self.atr[0] * self.atrdist_target
                self.pstop = self.data.close[0] + pdist_stop
                self.ptarget = self.data.close[0] + pdist_targ
            if self.check_if_downtrend():
                self.order = self.buy()
                self.isuptrend = False
                self.isdowntrend = True
                pdist_stop = self.atr[0] * self.atrdist_stop
                pdist_targ = self.atr[0] * self.atrdist_target
                self.pstop = self.data.close[0] - pdist_stop
                self.ptarget = self.data.close[0] - pdist_targ
        else:
            pclose = self.data.close[0]
            pstop = self.pstop
            ptarg = self.ptarget
            if self.isuptrend:
                if pclose < pstop or pclose > ptarg:
                    self.close()  # stop met - get out
                    self.isuptrend = False
                    self.isdowntrend = False
            if self.isdowntrend:
                if pclose > pstop or pclose < ptarg:
                    self.close()  # stop met - get out
                    self.isuptrend = False
                    self.isdowntrend = False

                
    def test_output(self):
        self.log_csv.to_csv(f'Data/{self.ticker}/{self.ticker}_{self.timeframe}_{self.strategy}.csv', index=False)

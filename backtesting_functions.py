from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

import backtrader as bt
import os, sys
import datetime
import pandas as pd
import numpy as np
import strategy_analizers.analizers as analizers


import backtrader_add.data_feeds.data_feeds as df

from backtrader_add.strategies.simple_strategy import SimpleStrategy
from backtrader_add.strategies.test_strategy import TestStrategy
from backtrader_add.strategies.buy_and_hold import BuyAndHold_1

file = ''




stocks1 = ['Aapl','Msft']
# ['Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm']
stocks = [x.upper() for x in stocks1]
print(stocks)
crypto = ["BTC", "ETH", "XRP", "BNB", "ADA"]
tickers = stocks
timeframes = ["1day", "4h", "2h", "1h", "30min", "15min", "5min", "1min"]


# tickers = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm', 'BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'ADA', 'MATIC']
# timeframes = ["1D", '4H', '2H', '1H', '30min', '15min', '5min', '1min']
strategies = [SimpleStrategy, BuyAndHold_1]



def saveplots(cerebro, numfigs=1, iplot=True, start=None, end=None,
             width=20, height=10, dpi=500, tight=True, use=None, file_path = 'test', **kwargs):

        from backtrader import plot
        if cerebro.p.oldsync:
            plotter = plot.Plot_OldSync(**kwargs)
        else:
            plotter = plot.Plot(**kwargs)

        figs = []
        for stratlist in cerebro.runstrats:
            for si, strat in enumerate(stratlist):
                rfig = plotter.plot(strat, figid=si * 100,
                                    numfigs=numfigs, iplot=iplot,
                                    start=start, end=end, use=use)
                figs.append(rfig)

        for fig in figs:
            for f in fig:
                f.savefig(file_path, bbox_inches='tight')
        return figs


# sample strategy used for plotting the data
def config_update(ticker, timeframe, strategy):
    data = {}
    data['ticker'] = ticker
    data['timeframe'] = timeframe
    data['strategy'] = strategy
    with open("config.json", "w") as f:
        json.dump(data, f)


def main (ticker, timeframe, strategy):
    ticker = ticker.upper()
    if timeframe == "1day":
        data = df.Data1day(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "30min":
        data = df.Data30min(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "5min":
        data = df.Data5min(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "15min":
        data = df.Data15min(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "1h":
        data = df.Data1hour(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "2h":
        data = df.Data2hour(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "4h": 
        data = df.Data4hour(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')
    elif timeframe == "1min":
        data = df.Data1min(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_new.csv')       
    else:
        print("error ", ticker, timeframe)
        return

    cerebro = bt.Cerebro()

    cerebro.adddata(data)
    cerebro.broker.set_cash(100000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    cerebro.addstrategy(strategy)
    # Add Analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe', timeframe= bt.TimeFrame.Months)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='mydrawdown')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='myroi')
    cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name='myrollingroi', timeframe= bt.TimeFrame.Months)
    results = cerebro.run()
    # get values from analyzers
    testresults_dict = analizers.prepare_testresults(strategy, ticker, timeframe, results)

    # for result in results:
    #     result.test_output()
    date_file = datetime.datetime.now()
    dt_string = date_file.strftime("%Y-%m-%d_%H:%M")
    saveplots(cerebro, file_path = f'results/graphs/{ticker}_{timeframe}_{strategy}_{dt_string}.png', volume=False) #run it
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    testresults_dict['total_return'] = 100 * (cerebro.broker.getvalue() - 100000)/100000
    testresults_dict['portfolio_return'] = cerebro.broker.getvalue()
    return testresults_dict


if __name__ == '__main__':
    log_df = pd.DataFrame()
    for strategy in strategies:
        for ticker in tickers:
            for timeframe in timeframes:
                config_update(ticker, timeframe, strategy.__name__)
                print(ticker, timeframe)
                one_result_dict = main (ticker, timeframe, strategy)
                log_df = log_df.append(one_result_dict, ignore_index=True)
    print(log_df.tail())
    date_file = datetime.datetime.now()
    dt_string = date_file.strftime("%Y-%m-%d_%H%M%S")
    log_df.to_csv(f'results/result_overview_{dt_string}.csv', index = False)
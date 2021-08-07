from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import analizers
import backtrader as bt
import datetime
import json
import numpy as np
import os
import pandas as pd
import sys

import backtrader_add.data_feeds.alpha_data_feeds as alpha_df

from backtrader_add.strategies.simple_strategy import SimpleStrategy
from backtrader_add.strategies.test_strategy import TestStrategy
from backtrader_add.strategies.buy_and_hold import BuyAndHold_1

# tickers = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm', 'BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'ADA', 'MATIC']
stocks = list()
tickers = ['BTC', 'ETH']
crypto = ['BTC','ETH']
# timeframes = ["1D", '4H', '2H', '1H', '30min', '15min', '5min', '1min']
timeframes = ["1D"]
strategies = [SimpleStrategy, TestStrategy, BuyAndHold_1]

def saveplots(cerebro, numfigs=1, iplot=True, start=None, end=None,
             width=16, height=9, dpi=300, tight=True, use=None, file_path = 'test', **kwargs):

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

def config_update(ticker, timeframe, strategy):
    """TODO

    Args:
        ticker ([type]): [description]
        timeframe ([type]): [description]
        strategy ([type]): [description]
    """
    data = {}
    data['ticker'] = ticker
    data['timeframe'] = timeframe
    data['strategy'] = strategy
    with open("config.json", "w") as f:
        json.dump(data, f)


def main (ticker, timeframe, strategy):
    """TODO

    Args:
        ticker ([type]): [description]
        timeframe ([type]): [description]
        strategy ([type]): [description]

    Returns:
        [type]: [description]
    """
    if timeframe == "1D":
        if ticker in stocks:
            data = alpha_df.VDailyData(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')
        elif ticker in crypto:
            data = alpha_df.VDailyDataCrypto(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "5M":
        if ticker in stocks:
            data = alpha_df.V5minData(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')
        elif ticker in crypto:
            data = alpha_df.VIntradayDataCrypto(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')        
    elif timeframe == "15M":
        data = alpha_df.V15minData(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "1H":
        data = alpha_df.VHourlyData(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "60min":
        data = alpha_df.VIntradayDataCrypto(dataname=f'input_data/{ticker}/{ticker}_{timeframe}_reversed.csv')    
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
    saveplots(cerebro, file_path = f'results/graphs/{ticker}_{timeframe}_{dt_string}.png') #run it
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    testresults_dict['total_return'] = 100 * (cerebro.broker.getvalue() - 100000)/100000
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
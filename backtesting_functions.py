from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

import backtrader as bt
import os, sys
import datetime
import pandas as pd
import alphaClasses
import strategyClasses
import numpy as np
import analizers

file = ''


# tickers = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm', 'BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'ADA', 'MATIC']
stocks = list()
tickers = ['BTC', 'ETH']
crypto = ['BTC','ETH']
# timeframes = ["1D", '4H', '2H', '1H', '30min', '15min', '5min', '1min']
timeframes = ["1D" ]
strategies = [strategyClasses.SimpleStrategy, strategyClasses.BuyAndHold_1]


# sample strategy used for plotting the data
def config_update(ticker, timeframe, strategy):
    data = {}
    data['ticker'] = ticker
    data['timeframe'] = timeframe
    data['strategy'] = strategy
    with open("config.json", "w") as f:
        json.dump(data, f)


def main (ticker, timeframe, strategy):

    if timeframe == "1D":
        if ticker in stocks:
            data = alphaClasses.AlphaVDailyData(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')
        elif ticker in crypto:
            data = alphaClasses.AlphaVDailyDataCrypto(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "5M":
        data = alphaClasses.AlphaV5minData(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "15M":
        data = alphaClasses.AlphaV15minData(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "1H":
        data = alphaClasses.AlphaVHourlyData(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "1DC":
        data = alphaClasses.AlphaVDailyDataCrypto(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')
    elif timeframe == "60min":
        data = alphaClasses.AlphaVIntradayDataCrypto(dataname=f'data/{ticker}/{ticker}_{timeframe}_reversed.csv')    
    else:
        print("error ", ticker, timeframe)
        return

    cerebro = bt.Cerebro()

    cerebro.adddata(data)
    cerebro.broker.set_cash(100000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
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

    figure = cerebro.plot()[0][0].savefig('data/TSLA/example.png')
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
    dt_string = date_file.strftime("%Y-%m-%d_%H:%M")
    log_df.to_csv(f'result_overview_{dt_string}.csv', index = False)
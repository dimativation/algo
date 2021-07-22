from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

import backtrader as bt
import os, sys
import datetime
import pandas as pd
import alphaClasses
import strategyClasses

file = ''


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
        data = alphaClasses.AlphaVDailyData(dataname=f'data/{ticker}/{ticker}_{timeframe}.csv')
    if timeframe == "5M":
        data = alphaClasses.AlphaV5minData(dataname=f'data/{ticker}/{ticker}_{timeframe}.csv')
    if timeframe == "15M":
        data = alphaClasses.AlphaV15minData(dataname=f'data/{ticker}/{ticker}_{timeframe}.csv')
    if timeframe == "1H":
        data = alphaClasses.AlphaVHourlyData(dataname=f'data/{ticker}/{ticker}_{timeframe}.csv')
    if timeframe == "1DC":
        data = alphaClasses.AlphaVDailyDataCrypto(dataname=f'data/{ticker}/{ticker}_{timeframe}.csv')

    cerebro = bt.Cerebro()

    cerebro.adddata(data)
    cerebro.broker.set_cash(100000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
    cerebro.addstrategy(strategyClasses.SimpleStrategy)

    config_update(ticker, timeframe, 'SimpleStrategy')


    results = cerebro.run()
    #
    # for result in results:
    #     result.test_output()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()


if __name__ == '__main__':
    main ('TSLA', "1D", "")

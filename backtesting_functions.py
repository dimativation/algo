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

file = ''


# sample strategy used for plotting the data


def config_update(ticker, timeframe, strategy):
    data = {}
    data['ticker'] = ticker
    data['timeframe'] = timeframe
    data['strategy'] = strategy
    with open("config.json", "w") as f:
        json.dump(data, f)

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
    cerebro.addstrategy(strategy)
    # Add Analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe', timeframe= bt.TimeFrame.Months)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='mydrawdown')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='myroi')
    cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name='myrollingroi', timeframe= bt.TimeFrame.Months)
    config_update(ticker, timeframe, strategy.__name__)
    results = cerebro.run()
    # get values from analyzers
    testresults_dict = prepare_testresults(strategy, ticker, timeframe, results)

    # for result in results:
    #     result.test_output()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # #figure = cerebro.plot()[0][0].savefig('data/TSLA/example.png')
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    testresults_dict['total_return'] = 100 * (cerebro.broker.getvalue() - 100000)/100000
    return testresults_dict


if __name__ == '__main__':
    timeframes = ["1D"]
    tickers = ['TSLA']
    strategies = [strategyClasses.SimpleStrategy, strategyClasses.BuyAndHold_1]
    log_df = pd.DataFrame()
    for strategy in strategies:
        for ticker in tickers:
            for timeframe in timeframes:
                print(ticker, timeframe)
                one_result_dict = main (ticker, timeframe, strategy)
                log_df = log_df.append(one_result_dict, ignore_index=True)
    print(log_df.tail())
    date_file = datetime.datetime.now()
    dt_string = date_file.strftime("%Y-%m-%d_%H:%M")
    log_df.to_csv(f'result_overview_{dt_string}.csv', index = False)
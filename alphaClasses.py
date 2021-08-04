import backtrader as bt
import os, sys
import datetime
import pandas as pd

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
        # ('close', 4),
        # ('adj-close', 5),
        ('close', 5),  # just testing
        ('volume', 6),
        ('div', 7),
        ('split', 8),
        ('openinterest', -1),
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
        # ('close', 4),
        # ('adj-close', 5),
        ('close', 4),  # just testing
        ('volume', -1),
        ('openinterest', -1)
    )

class AlphaVIntradayDataCrypto(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 60),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),  # just testing
        ('volume', 5),
        ('openinterest', -1),
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
        # ('adj-close', 5),
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
        # ('adj-close', 5),
        ('volume', 5),
        ('openinterest', -1),
    )

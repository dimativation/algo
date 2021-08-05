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
        ('open', 1),
        ('high', 2),
        ('low', 3),
        # ('close', 4),
        # ('adj-close', 5),
        ('close', 4),  # just testing
        ('volume', -1),
        ('div', -1),
        ('split', -1),
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

class AlphaV1hData(bt.feeds.GenericCSVData):
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
        ('volume', -1),
        ('openinterest', -1),
    )

class AlphaV2hData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 120),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),  # just testing
        ('volume', -1),
        ('openinterest', -1),
    )

class AlphaV4hData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 240),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),  # just testing
        ('volume', -1),
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

        ('volume', -1),
        ('openinterest', -1),
        ('separator', ','),

    )


class AlphaV15minData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 15),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        # ('adj-close', 5),
        ('volume', -1),
        ('openinterest', -1),
    )


class AlphaV5minData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 5),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        # ('adj-close', 5),
        ('volume', -1),
        ('openinterest', -1),
    )


class AlphaV1minData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        # ('adj-close', 5),
        ('volume', -1),
        ('openinterest', -1),
    )

class AlphaV30minData(bt.feeds.GenericCSVData):
    params = (
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 30),
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        # ('adj-close', 5),
        ('volume', -1),
        ('openinterest', -1),
    )
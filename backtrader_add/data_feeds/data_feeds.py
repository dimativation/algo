import backtrader as bt
import os, sys

class Data1day(bt.feeds.GenericCSVData):
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


class Data4hour(bt.feeds.GenericCSVData):
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


class Data2hour(bt.feeds.GenericCSVData):
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

class Data1hour(bt.feeds.GenericCSVData):
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



class Data30min(bt.feeds.GenericCSVData):
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


class Data15min(bt.feeds.GenericCSVData):
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


class Data5min(bt.feeds.GenericCSVData):
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


class Data1min(bt.feeds.GenericCSVData):
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


import backtrader as bt


class VDailyData(bt.feeds.GenericCSVData):
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
        ('openinterest', -1))


class VDailyDataCrypto(bt.feeds.GenericCSVData):
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
        ('volume', 5))


class VIntradayDataCrypto(bt.feeds.GenericCSVData):
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
        ('openinterest', -1))

class VHourlyData(bt.feeds.GenericCSVData):
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
        ('separator', ','))


class V15minData(bt.feeds.GenericCSVData):
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
        ('openinterest', -1))


class V5minData(bt.feeds.GenericCSVData):
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
        ('openinterest', -1))

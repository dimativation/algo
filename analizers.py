import numpy as np


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

import json
from twelvedata import TDClient

td = TDClient(apikey="c822604c71594044b6d972cf97e9dae8")

stocks = ['Aapl','Msft','Wmt','Nke','Sbux','Tsla','Gme','Amc','C','V','Jpm']
crypto = ["BTC/USD", "ETH/USD", "XRP/USD", ""]


ts = td.time_series(
    symbol="BTC/USD, ETH/USD",
    interval="1day",
    outputsize=200,
    timezone="America/New_York",
    order="ASC"
)
main_pandas = ts.as_pandas()
print(main_pandas)
main_pandas.loc["BTC/USD"].to_csv("BTC_1day_new.csv")
main_pandas.loc["ETH/USD"].to_csv("ETH_1day_new.csv")

# main_pandas.to_csv("BABA_1day.csv")




# # with open("BABA_4h.csv", "w") as f:
# 	f.write(ts.as_csv())
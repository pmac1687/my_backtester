from backtest import Backtest
import pandas_datareader as pa_da

# from fastquant import get_stock_data, backtest
dates = ["01-01-2007", "07-09-2012"]
# df = get_stock_data("JFC", "2018-01-01", "2019-01-01")
df = pa_da.get_data_yahoo("aapl", "2018-01-01", "2019-01-01")

print(df)

l = Backtest("smac", [df], fast_period=15, slow_period=40)

# l = Backtest("rsi", [df], rsi_period=14, upper_bound=70, lower_bound=30)

l.graph(0)

print(l.name)

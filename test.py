from backtest import Backtest
import pandas_datareader as pa_da
from tapy import Indicators


# from fastquant import get_stock_data, backtest
dates = ["01-01-2007", "07-09-2012"]
# df = get_stock_data("JFC", "2018-01-01", "2019-01-01")
df = pa_da.get_data_yahoo("aapl", "2018-01-01", "2019-01-01")

print(df)

# l = Backtest("smac", [df], fast_period=15, slow_period=40)

# l = Backtest("macd", [df], fast_period=12, slow_period=26, period_signal=9)

# l = Backtest("bollinger_bands", [df], period=20, deviation=2)

# l = Backtest(
#    "fractal_alligator",
#    [df],
#    period_jaws=13,
#    period_teeth=8,
#    period_lips=5,
#    shift_jaws=8,
#    shift_teeth=5,
#    shift_lips=3,
# )

l = Backtest("accel/decel", [df])

# l = Backtest("rsi", [df], rsi_period=14, upper_bound=70, lower_bound=30)

# l.graph(0)

# print(l.name)

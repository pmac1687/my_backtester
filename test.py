from backtest import Backtest
import pandas_datareader as pa_da
from tapy import Indicators
import record


# from fastquant import get_stock_data, backtest
dates = ["01-01-2007", "07-09-2012"]
# df = get_stock_data("JFC", "2018-01-01", "2019-01-01")
df = pa_da.get_data_yahoo("aapl", "2018-01-01", "2019-01-01")

print(df)

# l = Backtest("smac", "aapl", [df], fast_period=range(10, 20), slow_period=range(35, 45))

# l = Backtest(
#    "macd",
#    "aapl",
#    [df],
#    fast_period=range(7, 14),
#    slow_period=range(20, 30, 2),
#    period_signal=range(7, 10),
# )
# r = [1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
# l = Backtest("bollinger_bands", "aapl", [df], period=range(10, 30), deviation=r,)

l = Backtest(
    "fractal_alligator",
    "aapl",
    [df],
    period_jaws=range(8, 14, 2),
    period_teeth=range(6, 10, 2),
    period_lips=range(3, 7, 2),
    shift_jaws=range(4, 10, 2),
    shift_teeth=range(3, 7, 2),
    shift_lips=range(3, 5, 2),
)

# l = Backtest("demarker", "aapl", [df], period=range(2, 25))

# l = Backtest("accel-decel", "aapl", [df])
# l = Backtest(
#    "rsi",
#    "aapl",
#    [df],
#    rsi_period=range(10, 15),
#    upper_bound=range(68, 72),
#    lower_bound=range(30, 32),
# )
#
record.write_to_csv(l)
# lst = [b, l]
#
# for i in lst:
#
#    record.write_to_csv(i)


# l = Backtest("rsi", [df], rsi_period=14, upper_bound=70, lower_bound=30)

# l.graph(0)

# print(l.name)

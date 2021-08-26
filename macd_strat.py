from tapy import Indicators
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calculate_portfolio import calculate_portfolio


def moving_average_convergence_divergence_strategy(obj, df):
    """
    macd_value:: where obj.fast_period ema - obj.slow_period ema
    macd_signal:: sma of macd_value over period of obj.signal_period
    strat:: when value crosses over signal
    """
    df = Indicators(df)
    df.macd(
        period_fast=obj.fast_period,
        period_slow=obj.slow_period,
        period_signal=obj.period_signal,
        column_name_signal="macd_signal",
        column_name_value="macd_value",
    )
    df = df.df
    df["divergence"] = df["macd_value"] - df["macd_signal"]
    df.fillna(0.0, inplace=True)
    df["signals"] = 0.0
    """
    if div goes from positive to negative, short
    if div goes from negative to positive, long
    """
    for i in range(len(df)):
        if df["macd_signal"][i] != 0.0 and df["macd_signal"][i - 1] != 0.0:
            if df["divergence"][i] > 0.0 and df["divergence"][i - 1] < 0.0:
                df["signals"][i] = 1.0
            if df["divergence"][i] < 0.0 and df["divergence"][i - 1] > 0.0:
                df["signals"][i] = -1.0
    calculate_portfolio(obj, df, "tapy")
    graph(df)
    print(df["long_capital"])


def graph(df):
    plt.figure()
    plt.subplot(311)
    plt.plot(df.index, df["Close"], color="black", label="close")
    plt.subplot(312)
    plt.plot(df.index, df["macd_value"], color="red", label="value")
    plt.plot(df.index, df["macd_signal"], color="blue", label="signal")
    plt.legend()
    plt.subplot(313)
    plt.bar(df.index, df["divergence"])
    plt.show()


# (self, period_fast=12, period_slow=26, period_signal=9, column_name_value='macd_value', column_name_signal='macd_signal')

if __name__ == "__main__":
    pass

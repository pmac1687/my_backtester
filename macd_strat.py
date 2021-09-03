from tapy import Indicators
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calculate_portfolio import calculate_portfolio


def moving_average_convergence_divergence_strategy(obj, df_og):
    """
    macd_value:: where obj.fast_period ema - obj.slow_period ema
    macd_signal:: sma of macd_value over period of obj.signal_period
    strat:: when value crosses over signal
    """
    prepare_params(obj)
    obj.indicator = "tapy"
    for param in obj.tested_params:
        df = df_og.copy()
        fast_period = param["fast_period"]
        slow_period = param["slow_period"]
        period_signal = param["period_signal"]
        df["param"] = f"f:{fast_period} s:{slow_period} p:{period_signal}"
        df = Indicators(df)
        df.macd(
            period_fast=fast_period,
            period_slow=slow_period,
            period_signal=period_signal,
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


def prepare_params(obj):
    """
    obj.fast_period, obj.slow_period, obj.period_signal
    """
    if check(obj.fast_period) or check(obj.slow_period) or check(obj.period_signal):
        fast = convert_to_list(obj.fast_period)
        slow = convert_to_list(obj.slow_period)
        period = convert_to_list(obj.period_signal)
        obj.tested_params = make_combo_dict_arrays([fast, slow, period])
    else:
        obj.tested_params = make_combo_dict_arrays(
            [[obj.fast_period], [obj.slow_period], [obj.period_signal]]
        )


def make_combo_dict_arrays(arr):
    combos = [
        {"fast_period": x, "slow_period": y, "period_signal": z}
        for x in arr[0]
        for y in arr[1]
        for z in arr[2]
    ]

    return combos


def check(obj):
    """
    check if obj is instance of  range or list
    """
    if isinstance(obj, range) or isinstance(obj, list):
        return True
    else:
        return False


def convert_to_list(obj):
    res = [x for x in obj] if check(obj) else [obj]
    return res


if __name__ == "__main__":
    pass

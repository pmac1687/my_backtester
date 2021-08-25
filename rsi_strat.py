import matplotlib.pyplot as plt
import stockstats
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio

pd.options.mode.chained_assignment = None  # default='warn'


def rsi_upper_lower_bound_strategy(obj, df):
    """
    simple upper/lower bound strategy
    long:
    when rsi goes below lower, buy
    when rsi goes above upper, sell
    short:
    when rsi goes above upper, buy short
    when rsi goes below lower, exit short position
    upper/lower:: ints between 1-100
    period:: int == days 
    """
    stock = stockstats.StockDataFrame.retype(df)
    stock[f"rsi_{obj.rsi_period}"]
    del df[f"rs_{obj.rsi_period}"]
    del df["closepm"]
    del df["closenm"]
    del df["close_-1_d"]
    del df["close_-1_s"]
    del df[f"closepm_{obj.rsi_period}_smma"]
    del df[f"closenm_{obj.rsi_period}_smma"]
    df["signals"] = 0.0
    df["signals"][df[f"rsi_{obj.rsi_period}"] <= obj.lower_bound] = 1.0
    df["signals"][df[f"rsi_{obj.rsi_period}"] >= obj.upper_bound] = -1.0
    df["signals"][: obj.rsi_period] = 0.0
    print(df)
    calculate_portfolio(obj, df, "stockstats")


if __name__ == "__main__":
    pass

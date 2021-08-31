import matplotlib.pyplot as plt
import stockstats
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio

pd.options.mode.chained_assignment = None  # default='warn'


def rsi_upper_lower_bound_strategy(obj, df_og):
    """
    simple upper/lower bound strategy
    long:
    when rsi goes below lower, buy
    when rsi goes above upper, sell
    short:
    when rsi goes above upper, buy short
    when rsi goes below lower, exit short position
    upper/lower:: ints between 1-100
    rsi_period:: int == days 
    """
    prepare_params(obj)
    obj.indicator = "stockstats"
    for param in obj.tested_params:
        df = df_og.copy()
        print("df copy og", df)
        rsi_period = param["period"]
        upper_bound = param["upper"]
        lower_bound = param["lower"]
        df["param"] = f"p:{rsi_period} up:{upper_bound} low:{lower_bound}"
        stock = stockstats.StockDataFrame.retype(df)
        print("param", df["param"][-1])
        stock[f"rsi_{rsi_period}"]
        try:
            del df[f"rs_{rsi_period}"]
            del df["closepm"]
            del df["closenm"]
            del df["close_-1_d"]
            del df["close_-1_s"]
            del df[f"closepm_{rsi_period}_smma"]
            del df[f"closenm_{rsi_period}_smma"]
        except:
            pass
        df["signals"] = 0.0
        df["signals"][df[f"rsi_{rsi_period}"] <= lower_bound] = 1.0
        df["signals"][df[f"rsi_{rsi_period}"] >= upper_bound] = -1.0
        df["signals"][:rsi_period] = 0.0
        print(df)
        calculate_portfolio(obj, df, "stockstats")


def prepare_params(obj):
    """
    upper_bound, lower_bound, rsi_period
    if passing range for params, create list of all possible combos
    """
    if check(obj.rsi_period) or check(obj.lower_bound) or check(obj.upper_bound):
        period = (
            [x for x in obj.rsi_period] if check(obj.rsi_period) else [obj.rsi_period]
        )
        upper = (
            [x for x in obj.upper_bound]
            if check(obj.upper_bound)
            else [obj.upper_bound]
        )
        lower = (
            [x for x in obj.lower_bound]
            if check(obj.lower_bound)
            else [obj.lower_bound]
        )
        combos = [
            {"period": x, "upper": y, "lower": z}
            for x in period
            for y in upper
            for z in lower
        ]
        print(combos)
        obj.tested_params = combos
    else:
        obj.tested_params.append(
            {
                "period": obj.rsi_period,
                "upper": obj.upper_bound,
                "lower": obj.lower_bound,
            }
        )


def check(obj):
    """
    check if obj is instance of  range or list
    """
    if isinstance(obj, range) or isinstance(obj, list):
        return True
    else:
        return False


if __name__ == "__main__":
    pass

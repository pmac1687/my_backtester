from tapy import Indicators
import pandas as pd
import numpy as np
from calculate_portfolio import calculate_portfolio


def bollinger_band_breakout_strategy(obj, df_og):
    """
    when close breaks above bollinger_up, enter short position
    when close breaks below bollinger_bottom, enter long position
    bollinger_mid:: sma where period=obj.period 
    bollinger_up:: bollinger_mid plus obj.deviation
    bolinger_bottom:: bollinger_mid minus obj.deviation
    """
    prepare_params(obj)
    obj.indicator = "tapy"
    for param in obj.tested_params:
        df = df_og.copy()
        period = param["period"]
        deviation = param["deviation"]
        df["param"] = f"p:{period} d:{deviation}"
        df = Indicators(df)
        df.bollinger_bands(
            period=period,
            deviation=deviation,
            column_name_top="bollinger_up",
            column_name_mid="bollinger_mid",
            column_name_bottom="bollinger_bottom",
        )
        df = df.df
        df.fillna(0.0, inplace=True)
        df["signals"] = 0.0
        df["signals"][df["Close"] > df["bollinger_up"]] = -1.0
        df["signals"][df["Close"] < df["bollinger_bottom"]] = 1.0
        df["signals"][df["bollinger_mid"] == 0.0] = 0.0
        calculate_portfolio(obj, df, "tapy")


def prepare_params(obj):
    """
    obj.period, obj.deviation
    """
    if check(obj.period) or check(obj.deviation):
        period = convert_to_list(obj.period)
        deviation = convert_to_list(obj.deviation)
        obj.tested_params = make_combo_dict_arrays([period, deviation])
    else:
        obj.tested_params = make_combo_dict_arrays([[obj.deviation], [obj.period]])


def make_combo_dict_arrays(arr):
    combos = [{"period": x, "deviation": y} for x in arr[0] for y in arr[1]]

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

from tapy import Indicators
import pandas as pd
import numpy as np
from calculate_portfolio import calculate_portfolio


def bollinger_band_breakout_strategy(obj, df):
    """
    when close breaks above bollinger_up, enter short position
    when close breaks below bollinger_bottom, enter long position
    bollinger_mid:: sma where period=obj.period 
    bollinger_up:: bollinger_mid plus obj.deviation
    bolinger_bottom:: bollinger_mid minus obj.deviation
    """
    df = Indicators(df)
    df.bollinger_bands(
        period=obj.period,
        deviation=obj.deviation,
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


if __name__ == "__main__":
    pass

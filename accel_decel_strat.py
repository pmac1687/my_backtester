import matplotlib.pyplot as plt
from tapy import Indicators
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio


def accel_decel_strategy(obj, df):
    """
    strategy: look for fractals in a/d for buy/sell positions
              when it swings opposite positive/negative,
              look for new opposite fractal to exit position
    AC:: sma of awesome accel over 5 periods
    """
    df = Indicators(df)
    df.accelerator_oscillator(column_name="a/d")
    df = df.df
    df.fillna(0.0, inplace=True)
    long = False
    short = False
    df["signals"] = 0.0
    for i in range(len(df)):
        if df["a/d"][i] != 0.0 and i < (len(df) - 3):
            if (
                df["a/d"][i]
                and df["a/d"][i + 1]
                and df["a/d"][i + 2]
                and df["a/d"][i + 3]
            ) < 0.0:
                if (
                    df["a/d"][i]
                    < df["a/d"][i + 1]
                    < df["a/d"][i + 2]
                    < df["a/d"][i + 3]
                    and long == False
                ):
                    df["signals"][i + 3] = 1.0
                    long = True
                    short = False

            if (
                df["a/d"][i]
                and df["a/d"][i + 1]
                and df["a/d"][i + 2]
                and df["a/d"][i + 3]
            ) > 0.0:
                if (
                    df["a/d"][i]
                    < df["a/d"][i + 1]
                    < df["a/d"][i + 2]
                    < df["a/d"][i + 3]
                    and short == False
                ):
                    df["signals"][i + 3] = -1.0
                    short = True
                    long = False

    calculate_portfolio(obj, df, "tapy")
    print(df["long_p-l"][df["long_p-l"] != 0.0])


if __name__ == "__main__":
    pass

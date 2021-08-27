import matplotlib.pyplot as plt
from tapy import Indicators
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio


def demarker_strategy(obj, df):
    """
    strategy: if demarker goes above 70 sell short
              if demarker goes below 30 buy long 
    """
    df = Indicators(df)
    df.de_marker(period=obj.period, column_name="dem")
    df = df.df
    df.fillna(0.0, inplace=True)
    long = False
    short = False
    df["signals"] = 0.0
    for i in range(len(df)):
        if df["dem"][i] != 0.0:
            if df["dem"][i] > 0.70 and short == False:
                df["signals"][i] = -1.0
                short = True
                long = False
            if df["dem"][i] < 0.30 and long == False:
                df["signals"][i] = 1.0
                long = True
                short = False
    calculate_portfolio(obj, df, "tapy")
    print(df["signals"][df["signals"] == 1.0])


if __name__ == "__main__":
    pass

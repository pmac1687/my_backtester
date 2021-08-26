import matplotlib.pyplot as plt
from tapy import Indicators
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio


def fractal_signal_when_correlated_to_alligator_strat(obj, df):
    """
    strat: enter long if fractal low is below alligator teeth
           sell short if fractal high is above alligator teeth 
           reverse for exiting positions.
    alligator_jaw:: smma where period=period_jaws, and timeshift=shift_jaws
    alligator_teeth:: smma where period=period_teeth, and timeshift=shift_teeth
    alligator_lips:: smma where period=period_lips, and timeshift=shift_lips
    """
    df["date"] = df.index
    df.index = range(len(df))
    df = Indicators(df)
    df.alligator(
        period_jaws=obj.period_jaws,
        period_teeth=obj.period_teeth,
        period_lips=obj.period_lips,
        shift_jaws=obj.shift_jaws,
        shift_teeth=obj.shift_teeth,
        shift_lips=obj.shift_jaws,
        column_name_jaws="alligator_jaw",
        column_name_teeth="alligator_teeth",
        column_name_lips="alligator_lips",
    )
    df.fractals(column_name_high="fractals_high", column_name_low="fractals_low")
    df = df.df
    print(df)
    df.fillna(0.0, inplace=True)
    df["signals"] = 0.0
    for i in range(len(df)):
        if df["alligator_teeth"][i] != 0:
            if (df["fractals_high"][i] == True) and (
                df["Close"][i] > df["alligator_teeth"][i]
            ):
                # because a fractal is only assumed if two days in future are lower
                df["signals"][i + 2] = -1.0
            if (df["fractals_low"][i] == True) and (
                df["Close"][i] < df["alligator_teeth"][i]
            ):
                # because a fractal is only assumed if two days in future are lower
                df["signals"][i + 2] = 1.0
    calculate_portfolio(obj, df, "tapy")


# period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='alligator_jaw', column_name_teeth='alligator_teeth', column_name_lips='alligator_lips')

if __name__ == "__main__":
    pass

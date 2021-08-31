import matplotlib.pyplot as plt
from tapy import Indicators
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio


def fractal_signal_when_correlated_to_alligator_strat(obj, df_og):
    """
    strat: enter long if fractal low is below alligator teeth
           sell short if fractal high is above alligator teeth 
           reverse for exiting positions.
    alligator_jaw:: smma where period=period_jaws, and timeshift=shift_jaws
    alligator_teeth:: smma where period=period_teeth, and timeshift=shift_teeth
    alligator_lips:: smma where period=period_lips, and timeshift=shift_lips
    """
    prepare_params(obj)
    obj.indicator = "tapy"
    for param in obj.tested_params:
        df = df_og.copy()
        period_jaws = param["period_jaws"]
        period_teeth = param["period_teeth"]
        period_lips = param["period_lips"]
        shift_jaws = param["shift_jaws"]
        shift_teeth = param["shift_teeth"]
        shift_lips = param["shift_lips"]
        df[
            "param"
        ] = f"pj:{period_jaws} pt:{period_teeth} pl:{period_lips} sj:{shift_jaws} st:{shift_teeth} sl:{shift_lips}"
        df["date"] = df.index
        df.index = range(len(df))
        df = Indicators(df)
        df.alligator(
            period_jaws=period_jaws,
            period_teeth=period_teeth,
            period_lips=period_lips,
            shift_jaws=shift_jaws,
            shift_teeth=shift_teeth,
            shift_lips=shift_jaws,
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


def prepare_params(obj):
    """
    obj.period_jaws,
    obj.period_teeth,
    obj.period_lips,
    obj.shift_jaws,
    obj.shift_teeth,
    obj.shift_lips,
    """
    if (
        check(obj.period_jaws)
        or check(obj.period_teeth)
        or check(obj.period_lips)
        or check(obj.shift_jaws)
        or check(obj.shift_teeth)
        or check(obj.shift_lips)
    ):
        p_jaws = convert_to_list(obj.period_jaws)
        p_teeth = convert_to_list(obj.period_teeth)
        p_lips = convert_to_list(obj.period_lips)
        s_jaws = convert_to_list(obj.shift_jaws)
        s_teeth = convert_to_list(obj.shift_teeth)
        s_lips = convert_to_list(obj.shift_lips)
        obj.tested_params = make_combo_dict_arrays(
            [p_jaws, p_teeth, p_lips, s_jaws, s_teeth, s_lips]
        )
    else:
        obj.tested_params = make_combo_dict_arrays(
            [
                [obj.period_jaws],
                [obj.period_teeth],
                [obj.period_lips],
                [obj.shift_jaws],
                [obj.shift_teeth],
                [obj.shift_lips],
            ]
        )


def make_combo_dict_arrays(arr):
    combos = [
        {
            "period_jaws": x,
            "period_teeth": y,
            "period_lips": z,
            "shift_jaws": a,
            "shift_teeth": b,
            "shift_lips": c,
        }
        for x in arr[0]
        for y in arr[1]
        for z in arr[2]
        for a in arr[3]
        for b in arr[4]
        for c in arr[5]
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

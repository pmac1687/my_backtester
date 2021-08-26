from tapy import Indicators
import pandas as pd
import numpy as np
import stockstats
import matplotlib.pyplot as plt

import mac_strat
import rsi_strat
import macd_strat
import bollinger_bands_strat
import alligator_fractal_strat
import accel_decel_strat

pd.options.mode.chained_assignment = None  # default='warn'


class Backtest:
    def __init__(
        self,
        name,
        dfs,
        fast_period=0,
        slow_period=0,
        rsi_period=0,
        upper_bound=0,
        lower_bound=0,
        period_signal=0,
        period=0,
        deviation=0,
        period_jaws=0,
        period_teeth=0,
        period_lips=0,
        shift_jaws=0,
        shift_teeth=0,
        shift_lips=0,
    ):
        self.name = name
        self.dfs = dfs
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.rsi_period = rsi_period
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.period_signal = period_signal
        self.period = period
        self.deviation = deviation
        self.period_jaws = period_jaws
        self.period_teeth = period_teeth
        self.period_lips = period_lips
        self.shift_jaws = shift_jaws
        self.shift_teeth = shift_teeth
        self.shift_lips = shift_lips
        if self.name == "smac":
            for df in self.dfs:
                mac_strat.moving_average_crossover(self, df, "sma")

        if self.name == "emac":
            for df in self.dfs:
                mac_strat.moving_average_crossover(self, df, "ema")

        if self.name == "rsi":
            for df in self.dfs:
                rsi_strat.rsi_upper_lower_bound_strategy(self, df)

        if self.name == "macd":
            for df in self.dfs:
                macd_strat.moving_average_convergence_divergence_strategy(self, df)

        if self.name == "bollinger_bands":
            for df in self.dfs:
                bollinger_bands_strat.bollinger_band_breakout_strategy(self, df)

        if self.name == "fractal_alligator":
            for df in self.dfs:
                alligator_fractal_strat.fractal_signal_when_correlated_to_alligator_strat(
                    self, df
                )

        if self.name == "accel/decel":
            for df in self.dfs:
                accel_decel_strat.accel_decel_strategy(self, df)

    def graph(self, ind):
        if self.name == "smac" or "emac":
            mac_strat.graph_smac(self, ind)


if __name__ == "__main__":
    pass


from tapy import Indicators
import stockstats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

import mac_strat
import rsi_strat

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
    ):
        self.name = name
        self.dfs = dfs
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.rsi_period = rsi_period
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        if self.name == "smac":
            for df in self.dfs:
                mac_strat.moving_average_crossover(self, df, "sma")

        if self.name == "emac":
            for df in self.dfs:
                mac_strat.moving_average_crossover(self, df, "ema")

        if self.name == "rsi":
            for df in self.dfs:
                rsi_strat.rsi_upper_lower_bound_strategy(self, df)

    def graph(self, ind):
        if self.name == "smac" or "emac":
            mac_strat.graph_smac(self, ind)


if __name__ == "__main__":
    pass


from tapy import Indicators
import stockstats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class Backtest:
    def __init__(
        self, name, dfs, fast_period=0, slow_period=0, long=False, short=False
    ):
        self.name = name
        self.dfs = dfs
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.long = long
        self.short = short
        if self.name == "smac":
            for df in self.dfs:
                self.simple_moving_average_crossover(df)

    def simple_moving_average_crossover(self, df):
        """
        fast_period:: int shorter ma period
        slow_period::int  longer ma period
        long::bool enter on long positions
        short::bool enter on short positions
        df:: single dataframe for one ticker
        strat: where fast goes above slow ma go long
        where it goes below short
        """
        df = Indicators(df)
        df.sma(period=self.fast_period, column_name="sma_fast", apply_to="Close")
        df.sma(period=self.slow_period, column_name="sma_slow", apply_to="Close")
        df = df.df
        df["trend"] = 0.0
        # if fast > slow 'trend' == 1.0, else 'trend' == 0.0
        df["trend"][self.fast_period :] = np.where(
            df["sma_fast"][self.fast_period :] > df["sma_slow"][self.fast_period :],
            1.0,
            0.0,
        )
        # when fast moves above slow signal will be 1.0 indicating buy
        # when fast moves below slow signal will be -1.0 indicating sell
        df["signals"] = df["trend"].diff()
        self.calculate_portfolio(df)

    def calculate_portfolio(self, df):
        initial_l = 100000
        position = 0
        df["long_only_profit"] = 0.0

    def graph(self, ind):
        if self.name == "smac":
            self.graph_smac(ind)

    def graph_smac(self, ind):
        df = self.dfs[ind]
        # plots for buys
        buy_xs = df.loc[df["signals"] == 1.0].index
        buy_ys = df.Close[buy_xs]
        # plots for sells
        sell_xs = df.loc[df["signals"] == -1.0].index
        sell_ys = df.Close[sell_xs]
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(df.index, df["Close"])
        ax1.plot(df.index, df["sma_slow"])
        ax1.plot(df.index, df["sma_fast"])
        ax1.plot(buy_xs, buy_ys, "^", markersize=10, color="g")
        ax1.plot(sell_xs, sell_ys, "*", markersize=10, color="r")
        plt.show()


if __name__ == "__main__":
    pass


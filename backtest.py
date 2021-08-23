from tapy import Indicators
import stockstats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


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
        """
        loop thru df, when we hit a 1.0 buy long.
        and than sell position when it comes to next -1.0
        reverse this for short positions.
        """
        # long positions
        long_capital = 100000.0
        long_position = 0.0
        df["long_positions"] = 0.0
        df["long_capital"] = 0.0
        df["long_p-l"] = 0.0
        for i in range(len(df)):
            if df["signals"][i] == 1.0:
                long_position = long_capital / df["Close"][i]

            if (df["signals"][i] == -1.0) and (long_position != 0.0):
                new_capital = long_position * df["Close"][i]
                df["long_p-l"][i] = (long_capital - new_capital) * -1
                long_capital = new_capital
                long_position = 0.0

            df["long_positions"][i] = long_position
            df["long_capital"][i] = long_capital
        df["long_value"] = sum(df["long_p-l"])
        """
        when selling short, get percent of close price of the day selling
        than take capital from when you bought the short times sell price percent
        """
        # short positions
        short_capital = 100000.0
        short_position = 0.0
        short_price = 0.0
        sell_price = 0.0
        df["short_positions"] = 0.0
        df["short_capital"] = 0.0
        df["short_p-l"] = 0.0
        df["short_price"] = 0.0
        df["sell_price"] = 0.0
        for b in range(len(df)):
            if df["signals"][b] == -1.0:
                short_position = short_capital / df["Close"][b]
                short_price = df["Close"][b]
                print("neg")

            if (df["signals"][b] == 1.0) and (short_position != 0.0):
                sell_price_percent = short_price / df["Close"][b]
                df["short_p-l"][b] = (
                    short_capital - (short_capital * sell_price_percent)
                ) * -1
                short_capital = short_capital * sell_price_percent
                short_position = 0.0
                sell_price = df["Close"][b]

            df["sell_price"][b] = sell_price
            df["short_price"][b] = short_price
            df["short_positions"][b] = short_position
            df["short_capital"][b] = short_capital
        df["short_value"] = sum(df["short_p-l"])
        print(df["long_capital"], df["short_capital"])

    def graph(self, ind):
        if self.name == "smac":
            self.graph_smac(ind)

    def graph_smac(self, ind):
        df = self.dfs[ind]
        """
        plots for buys
        signals either 1.0 or -1.0 for buy or sell 
        so we take all the signals where that is the case
        which idicates a buy or sell day to graph
        """
        # plots for buys
        buy_xs = df.loc[df["signals"] == 1.0].index
        buy_ys = df.Close[buy_xs]
        # plots for sells
        sell_xs = df.loc[df["signals"] == -1.0].index
        sell_ys = df.Close[sell_xs]
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        # lines
        ax1.plot(df.index, df["Close"])
        ax1.plot(df.index, df["sma_slow"])
        ax1.plot(df.index, df["sma_fast"])
        # markers
        ax1.plot(buy_xs, buy_ys, "^", markersize=10, color="g")
        ax1.plot(sell_xs, sell_ys, "*", markersize=10, color="r")
        # bars
        plt.show()


if __name__ == "__main__":
    pass


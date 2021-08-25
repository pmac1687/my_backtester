import matplotlib.pyplot as plt
from tapy import Indicators
import numpy as np
import pandas as pd
from calculate_portfolio import calculate_portfolio

pd.options.mode.chained_assignment = None  # default='warn'


def moving_average_crossover(obj, df, indicator):
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
    if indicator == "sma":
        df.sma(period=obj.fast_period, column_name="ma_fast", apply_to="Close")
        df.sma(period=obj.slow_period, column_name="ma_slow", apply_to="Close")
    if indicator == "ema":
        df.ema(period=obj.fast_period, column_name="ma_fast", apply_to="Close")
        df.ema(period=obj.slow_period, column_name="ma_slow", apply_to="Close")
    df = df.df
    df["trend"] = 0.0
    # if fast > slow 'trend' == 1.0, else 'trend' == 0.0
    df["trend"][obj.fast_period :] = np.where(
        df["ma_fast"][obj.fast_period :] > df["ma_slow"][obj.fast_period :], 1.0, 0.0,
    )
    # when fast moves above slow signal will be 1.0 indicating buy
    # when fast moves below slow signal will be -1.0 indicating sell
    df["signals"] = df["trend"].diff()
    calculate_portfolio(obj, df, "tapy")


def graph_smac(obj, ind):
    df = obj.dfs[ind]
    print(df.columns)
    plt.figure()
    """
    plot profit/loss bars
    df['short_p-l'], df['long_p-l']
    per trade and throughout run
    """
    # bars
    plt.subplot(313)
    # short p-l bars
    short_pl_inds = df.loc[df["short_p-l"] != 0.0].index
    short_pl = df["short_p-l"][short_pl_inds]
    short_x_ax = range(2, len(short_pl_inds) * 4, 4)
    plt.bar(short_x_ax, short_pl, color="#E67578", label="short pos profit/loss")

    pl_tot_arr = []
    pl_total = 0
    for p in range(len(short_pl)):
        print("pl", short_pl[p])
        pl_total += short_pl[p]
        pl_tot_arr.append(pl_total)
    print(pl_tot_arr)
    short_x_tot_ax = range(3, len(short_pl_inds) * 4, 4)
    plt.bar(short_x_tot_ax, pl_tot_arr, color="red", label="short p/l total")

    # short annotations
    for i in range(len(short_pl)):
        plt.text(short_x_ax[i] - 0.25, 0, f"{round(short_pl[i])}")
        plt.text(short_x_tot_ax[i] - 0.25, 0, f"{round(pl_tot_arr[i])}")

    # long p-l bars
    long_pl_inds = df.loc[df["long_p-l"] != 0.0].index
    long_pl = df["long_p-l"][long_pl_inds]
    long_x_ax = range(0, len(long_pl_inds) * 4, 4)
    plt.bar(long_x_ax, long_pl, color="#01FF01", label="long pos profit/loss")

    pl_tot_arr = []
    pl_total = 0
    for p in range(len(long_pl)):
        print("pl", long_pl[p])
        pl_total += long_pl[p]
        pl_tot_arr.append(pl_total)
    print(pl_tot_arr)
    long_x_tot_ax = range(1, len(long_pl_inds) * 4, 4)
    plt.bar(long_x_tot_ax, pl_tot_arr, color="green", label="long p/l total")

    # long annotation
    for i in range(len(long_pl)):
        plt.text(long_x_ax[i] - 0.25, 0, f"{round(long_pl[i])}")
        plt.text(long_x_tot_ax[i] - 0.25, 0, f"{round(pl_tot_arr[i])}")

    plt.legend()

    # volume bars
    plt.subplot(312)
    plt.bar(df.index, df["Volume"], label="volume")
    plt.legend()

    plt.subplot(311)
    """
    text annotation for p/l's of buys and sells
    """
    for i in range(len(long_pl_inds)):
        plt.text(
            long_pl_inds[i],
            df["Close"][long_pl_inds[i]] - 5,
            f"long={round(long_pl[i])}",
        )
    for i in range(len(short_pl_inds)):
        plt.text(
            short_pl_inds[i],
            df["Close"][short_pl_inds[i]] + 5,
            f"short={round(short_pl[i])}",
        )
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
    # lines
    plt.plot(df.index, df["Close"], color="black", label="close")
    plt.plot(df.index, df["ma_slow"], color="red", label="slow ma")
    plt.plot(df.index, df["ma_fast"], color="blue", label="fast ma")
    # markers
    plt.plot(buy_xs, buy_ys, "^", markersize=10, color="g", label="long pos crossover")
    plt.plot(
        sell_xs, sell_ys, "v", markersize=10, color="r", label="short pos crossover"
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    pass

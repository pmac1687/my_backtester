import sqlite3
import datetime
from backtest import Backtest
import record
import pandas as pd
from multiprocessing import Process

RES_ARR = []


def get_tickers():
    conn = sqlite3.connect("db/ohlcv.db")
    cur = conn.cursor()
    cur.execute(f"""select * from tickers limit {2};""")
    conn.commit()
    tickers = cur.fetchall()
    conn.close()

    return tickers


def conduct_test(tick):
    conn = sqlite3.connect("db/ohlcv.db")
    query = f"SELECT * FROM historical_ochlv WHERE id={tick[0]};"
    df = pd.read_sql_query(query, conn)
    df["id"] = tick[1]
    dates = []
    for i in range(len(df)):
        dat = datetime.datetime(df["year"][i], df["month"][i], df["day"][i])
        dates.append(dat)
    df["Date"] = dates
    # l = Backtest(
    #    "rsi",
    #    df["id"],
    #    [df],
    #    rsi_period=range(9, 15),
    #    upper_bound=range(65, 75),
    #    lower_bound=range(25, 35),
    # )
    l = Backtest("rsi", df["id"], [df], rsi_period=15, upper_bound=70, lower_bound=30)
    RES_ARR.append(l.df_results[0].iloc[-1])


if __name__ == "__main__":
    tickers = get_tickers()
    ps = []
    for tick in tickers:
        my_process = Process(target=conduct_test, args=(tick,))
        ps.append(my_process)
    for p in ps:
        p.start()
    for p in ps:
        p.join()

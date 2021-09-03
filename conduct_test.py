import sqlite3
import pandas as pd
import datetime
from backtest import Backtest
import record


def get_tickers(ticker_range):
    conn = sqlite3.connect("db/ohlcv.db")
    cur = conn.cursor()
    cur.execute(f"""select * from tickers limit {ticker_range};""")

    conn.commit()

    tickers = cur.fetchall()

    conn.close()

    return tickers


def get_tick_df(tick):
    conn = sqlite3.connect("db/ohlcv.db")
    query = f"SELECT * FROM historical_ochlv WHERE id={tick[0]};"

    df = pd.read_sql_query(query, conn)
    df["id"] = tick[1]
    dates = []
    for i in range(len(df)):
        dat = datetime.datetime(df["year"][i], df["month"][i], df["day"][i])
        dates.append(dat)
    df["date"] = dates
    return df


def conduct_backtest(df, test, args):
    test_df = Backtest(
        test,
        df["id"],
        [df],
        rsi_period=args[0],
        upper_bound=args[1],
        lower_bound=args[2],
    )
    record.write_to_csv(test_df)


def main(args, test, ticker_range):
    tickers = get_tickers(ticker_range)
    for tick in tickers:
        df = get_tick_df(tick)
        conduct_backtest(df, test, args)
        break


if __name__ == "__main__":
    """
    ticker_range:: number of tickers to testing
    standard:: Backtest("test","ticker",[dfs], args)
    args:: 'test_name', [args], ticker_range
    -------------------------------------------
    rsi:: Backtest("rsi",rsi_period=14,upper_bound=70,lower_bound=30)
    ------------------------------------------------------------------
    """
    args = [range(9, 15), range(65, 75), range(25, 35)]
    test = "rsi"
    ticker_range = 100
    main(args, test, ticker_range)


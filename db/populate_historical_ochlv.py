import pandas_datareader as pa_da
import csv
import asyncio
import time
from asgiref.sync import sync_to_async
import sqlite3
from fastquant import get_stock_data


def insert_df_db(df):
    conn = sqlite3.connect("ohlcv.db")
    for i in range(len(df)):
        conn.execute(
            f"""insert into historical_ochlv (
                        id,day,month,year,open,close,high,low,volume) values (
                        {int(df['ticker_id'][i])},{df['day'][i]},{df['month'][i]},{df['year'][i]},{df['open'][i]},
                        {df['close'][i]},{df['high'][i]},{df['low'][i]}, {df['volume'][i]}
                        );"""
        )

    conn.commit()
    conn.close()


async def main(tick_arr):
    for tick in tick_arr:
        print(tick)
        try:
            df = await sync_to_async(get_stock_data)(
                tick[1].lower(), "2019-8-20", "2021-8-20"
            )
            df["day"] = df.index.strftime("%d")
            df["month"] = df.index.strftime("%m")
            df["year"] = df.index.strftime("%Y")

            df["day"] = df["day"].apply(lambda x: int(x))
            df["month"] = df["month"].apply(lambda x: int(x))
            df["year"] = df["year"].apply(lambda x: int(x))
            df = df.fillna(0.0)

            # print(type(df["year"][0]))
            df["ticker_id"] = tick[0]
            print(tick[0], tick[1])
            insert_df_db(df)

        except Exception as e:
            print("exception:", e)
            continue


if __name__ == "__main__":
    arr = []
    with open("tickers.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            arr.append([row[0], row[1]])
    start_time = time.perf_counter()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(arr))

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")

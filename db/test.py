import pandas as pd
import psycopg2
import keys
import stockstats
from tapy import Indicators
import csv
import concurrent.futures
from psycopg2.pool import ThreadedConnectionPool
import pandas_datareader as pa_da
from asgiref.sync import sync_to_async
import asyncio
import time

from threading import Semaphore


def insert_df_db(df):
    conn = tcp.getconn()
    cur = conn.cursor()
    # cur.execute(f"select * from master_ticker_list limit 5;")
    arr = f""
    for row_index, row in df.iterrows():
        que = f"""insert into historical_stock_data ( ticker_id , date ,
                     open , close , high , low , volume , rsi_12 ,
                    rsi_6 , rsi_18 , rsi_24 , macd , macd_sig , macd_hist , boll ,
                     boll_ub , boll_lb , sma_10 , sma_50 , sma_200 , ema_50 , ema_10 ,
                      ema_200 , ao , atr , smma_5 , smma_50 , smma_200 , momentum ,
                       accel_oss , alligator_jaw , alligator_teeth , alligator_lips ,
                        gator_value1 , gator_value2 , f_high , f_low) values (
                            {row['ticker_id']},'{row['date'].strftime('%Y-%m-%d')}',{row['open']},{row['Close']},
                            {row['High']},{row['Low']},{row['Volume']},{row['rsi_12']},{row['rsi_6']},
                    {row['rsi_18']},{row['rsi_24']},{row['macd']},{row['macd_sig']},{row['macd_hist']},
                    {row['boll']},{row['boll_ub']},{row['boll_lb']},{row['sma_10']},{row['sma_50']},{row['sma_200']},
                    {row['ema_50']},{row['ema_10']},{row['ema_200']},{row['ao']},{row['atr']},{row['smma_5']},{row['smma_50']},{row['smma_200']},
                    {row['momentum']},{row['accel_oss']},{row['alligator_jaw']},{row['alligator_teeth']},{row['alligator_lips']},
                    {row['gator_value1']},{row['gator_value2']},{row['f_high']},{row['f_low']}); """

        arr += que

    # psql_pool.Pcursor().execute(arr)
    # cur.execute(arr)
    # print('updated:', cur.rowcount)
    # print(len(cur.query))
    # tcp.putconn(conn, close=False)
    # conn.commit()


async def main(tick_arr):
    # tick_arr[1] ==  'AA'
    # tick_arr[0]  == id

    for tick in tick_arr:
        try:
            df = await sync_to_async(pa_da.get_data_yahoo)(
                tick[1], "2017-8-20", "2021-8-20"
            )

            df["date"] = df.index
            df["ticker_id"] = tick[0]
            print(tick[0], tick[1])
            # df.index = range(len(df))
            # print(df.iloc[0]['date'].strftime("%Y-%m-%d"))
            # df = df.fillna(0)
            # df = df.replace("", 0)
            insert_df_db(df)

        except AttributeError as e:
            print(e)


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

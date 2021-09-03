import sqlite3


def execute_queries(arr):
    conn = sqlite3.connect("ohlcv.db")

    for que in arr:
        conn.execute(que)

    conn.close()


def main():
    tickers_table_query = """create table tickers (
                id int not null,
                ticker text not null
                );"""

    historical_ochlv_table_query = """ create table historical_ochlv (
                                    id int not null,
                                    year int,
                                    month int,
                                    day int,
                                    open decimal,
                                    close decimal,
                                    high decimal,
                                    low decimal,
                                    volume decimal
                                    ); """
    arr = [historical_ochlv_table_query]
    execute_queries(arr)


if __name__ == "__main__":
    main()

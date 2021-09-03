import sqlite3
import csv


def get_tickers():
    arr = []
    with open("tickers.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            arr.append([row[0], row[1]])

    return arr


def populate_ticker_table(tickers):
    conn = sqlite3.connect("ohlcv.db")
    for tick in tickers:
        conn.execute(
            f"""insert into tickers (
                    id,ticker) values (
                    {tick[0]},'{tick[1]}'
                    );"""
        )

    conn.commit()
    conn.close()


def main():
    tickers = get_tickers()
    populate_ticker_table(tickers)


if __name__ == "__main__":
    main()

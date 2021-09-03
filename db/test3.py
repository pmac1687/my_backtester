import sqlite3

conn = sqlite3.connect("ohlcv.db")
cur = conn.cursor()
cur.execute(
    f"""select count(*) from tickers where id not in (select id from historical_ochlv);"""
)

conn.commit()

print(cur.fetchone())


conn.close()

# f"""select * from tickers where id not in (select id from historical_ochlv);"""

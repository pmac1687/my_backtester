import sqlite3

conn = sqlite3.connect("ohlcv.db")
conn.execute(f"""select *  historical_ochlv;""")
conn.commit()
conn.close()

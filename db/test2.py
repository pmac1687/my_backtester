import sqlite3
import time

start_time = time.perf_counter()

conn = sqlite3.connect("ohlcv.db")

cur = conn.cursor()

cur.execute(f"""select * from historical_ochlv where day in (1,4,7,9);""")

conn.commit()

print(cur.fetchall())

conn.close()

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed run time: {elapsed_time} seconds")

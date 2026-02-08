import sqlite3
import pandas as pd
import json
import matplotlib.pyplot as plt

conn = sqlite3.connect('crypto.db')
cursor = conn.cursor()

df = pd.read_sql_query('SELECT * FROM data', conn)
df = df.filter(items=['ticker_id', 'price', 'timestamp'])
df = df.pivot(index='timestamp', columns='ticker_id', values='price')

df.plot(figsize=(10,6), marker='o', title="Crypto Prices Over Time")
plt.xlabel("Time")
plt.ylabel("Price")
plt.title("Price over time")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


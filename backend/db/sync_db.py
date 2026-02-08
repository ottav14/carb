import requests
import json
import pandas as pd
import sqlite3
import time
from datetime import datetime

max_data_rows = 1000000
conn = sqlite3.connect('/home/dom/projects/carb/backend/db/crypto.db')
cursor = conn.cursor()

def get_row_count(table):
    cursor.execute(f'SELECT COUNT(*) FROM {table};')
    return cursor.fetchone()[0]


url = 'https://api.coinbase.com/api/v3/brokerage/market/products'

# Grab new entries
res = requests.get(url)
data = res.json()
df = pd.DataFrame(data['products']).filter(items=['product_id', 'price', 'volume_24h'])
entry_count = df.shape[0]

# Write new entries to db
tickers_start_order = get_row_count('tickers')
data_start_order = get_row_count('data')
for i, row in df.iterrows():
    # Update ticker
    cursor.execute('INSERT OR IGNORE INTO tickers (ticker) VALUES (?)', 
                  (row['product_id'],))

    # Get id
    cursor.execute('SELECT id FROM tickers WHERE ticker = (?)',
                  (row['product_id'],))
    ticker_id = cursor.fetchone()[0]

    # Update data
    cursor.execute('INSERT INTO data (ticker_id, price, volume) VALUES (?, ?, ?)',
                  (ticker_id, row['price'], row['volume_24h']))





tickers_end_order = get_row_count('tickers')
data_end_order = get_row_count('data')
tickers_added_count = tickers_end_order - tickers_start_order
data_added_count = data_end_order - data_start_order
deleted_count = 0

# Maintain size constraints
if(data_end_order > max_data_rows):
    difference = data_end_order - max_data_rows
    start_order = get_row_count('data')
    cursor.execute(f"""
        DELETE FROM data
        WHERE id IN (
            SELECT id 
            FROM data
            ORDER BY timestamp ASC
            LIMIT {difference}
        );
        """)
    end_order = get_row_count('data')
    deleted_count = start_order - end_order



conn.commit()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"""{timestamp}
---------------------
Tickers added: {tickers_added_count}
Total tickers: {tickers_end_order}
Data added: {data_added_count}
Total data: {data_end_order-deleted_count}
Culled: {deleted_count}
""")

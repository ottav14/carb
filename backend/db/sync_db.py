import requests
import json
import pandas as pd
import sqlite3
import time
from datetime import datetime

max_data_rows = 1000000
conn = sqlite3.connect('/home/dom/projects/carb/backend/db/data.db')
cursor = conn.cursor()

coinbase_url = 'https://api.coinbase.com/api/v3/brokerage/market/products'
polymarket_prices_url = 'https://clob.polymarket.com/price'

def get_row_count(table):
    cursor.execute(f'SELECT COUNT(*) FROM {table};')
    return cursor.fetchone()[0]

def sync_polymarket_events():
    res_count = 1
    offset = 0
    limit = 100
    total = 0
    while res_count > 0:
        url = f'https://gamma-api.polymarket.com/events?limit={limit}&offset={offset}&order=creationDate&ascending=false'
        offset += limit
        res = requests.get(url)
        data = pd.DataFrame(res.json())

        cursor.execute('SELECT COUNT(*) FROM polymarket_events')
        start_count = cursor.fetchone()[0]

        for i, row in data.iterrows():
            event_id = int(row['id'])
            cursor.execute("SELECT EXISTS(SELECT 1 FROM polymarket_events WHERE event_id = ?)",
                          (event_id,))

            exists = cursor.fetchone()[0]
            if exists: break

            cursor.execute('INSERT OR IGNORE INTO polymarket_events (event_id) VALUES (?)',
                          (event_id,))


        cursor.execute('SELECT COUNT(*) FROM polymarket_events')
        res_count = cursor.fetchone()[0] - start_count
        total += res_count

    print('Polymarket Events Added:', res_count)


def sync_polymarket_markets():
    cursor.execute('SELECT event_id FROM polymarket_events')
    event_ids = cursor.fetchall()

    res_count = 1
    offset = 0
    limit = 100
    total = 0
    for event_id in event_ids:
        url = f'https://gamma-api.polymarket.com/markets/{event_id[0]}'
        offset += limit
        res = requests.get(url)
        data = res.json()

        print(data)



# Polymarket
sync_polymarket_events()
sync_polymarket_markets()

# Grab new entries
res = requests.get(coinbase_url)
data = res.json()
df = pd.DataFrame(data['products'])
entry_count = df.shape[0]

# Write new entries to db
coinbase_start_order = get_row_count('coinbase')
for i, row in df.iterrows():
    # Update data
    cursor.execute('INSERT INTO coinbase (ticker, price, volume) VALUES (?, ?, ?)',
                  (row['product_id'], row['price'], row['volume_24h']))



coinbase_end_order = get_row_count('coinbase')
coinbase_added_count = coinbase_end_order - coinbase_start_order
deleted_count = 0

# Maintain size constraints
if(coinbase_end_order > max_data_rows):
    difference = data_end_order - max_data_rows
    start_order = get_row_count('coinbase')
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
print(f"""
Coinbase Rows Added: {coinbase_added_count}
Coinbase Rows Culled: {deleted_count}
Coinbase Total rows: {coinbase_end_order-deleted_count}
""")

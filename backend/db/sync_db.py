import requests
import json
import pandas as pd
import sqlite3
import time
from datetime import datetime, timezone

max_data_rows = 1000000
conn = sqlite3.connect('/home/dom/projects/carb/backend/db/data.db')
cursor = conn.cursor()

coinbase_url = 'https://api.coinbase.com/api/v3/brokerage/market/products'
polymarket_prices_url = 'https://clob.polymarket.com/price'

def get_row_count(table):
    cursor.execute(f'SELECT COUNT(*) FROM {table};')
    return cursor.fetchone()[0]

def get_iso_today():
    start_of_today = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
    )
    return start_of_today.isoformat().replace("+00:00", "Z")

def get_unix_today():
    start_of_today_utc = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
    )
    return int(start_of_today_utc.timestamp())


def sync_kalshi():
    limit = 1000
    offset = 0
    total = 0
    res_count = 1
    today = get_unix_today()
    while res_count > 0:
        url = f'https://api.elections.kalshi.com/trade-api/v2/markets?limit={limit}&cursor={offset}&min_created_ts={today}'
        res = requests.get(url)
        data = res.json()
        df = pd.DataFrame(data['markets'])
        
        for i, row in df.iterrows():
            cursor.execute('INSERT OR IGNORE INTO kalshi (ticker, title, created_time, yes_bid, yes_ask, no_bid, no_ask) VALUES (?, ?, ?, ?, ?, ?, ?)',
                          (row['ticker'], row['title'], row['created_time'], row['yes_bid'], row['yes_ask'], row['no_bid'], row['no_ask']))

        offset += limit
        res_count = df.shape[0]
        total += df.shape[0]
        time.sleep(0.1)

    conn.commit()
    print(f'Kalshi Markets Found: {total}')
    


# Kalshi
sync_kalshi()


def sync_coinbase():
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

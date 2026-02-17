import requests
import time
import sqlite3
import asyncio

semaphore = asyncio.Semaphore(5)
conn = sqlite3.connect('/home/dom/projects/carb/backend/db/data.db')
cursor = conn.cursor()

async def api_call(url):
    async with semaphore:
        response = requests.get(url)
        data = response.json()
        await asyncio.sleep(0.2)
        return data

async def get_paginated(base_url, key):
    all_data = []
    cursor = None

    while True:
        # Build URL with cursor if we have one
        url = f"{base_url}"
        if cursor:
            url += f"&cursor={cursor}"

        data = await api_call(url)

        if key not in data:
            print('ERROR', data)
            break

        all_data.extend(data[key])

        # Check if there are more pages
        cursor = data.get('cursor')
        if not cursor:
            break

        print(f"Fetched {len(data[key])} events, total: {len(all_data)}")
        time.sleep(0.1)

    return all_data

async def get_markets(events):
    all_data = []
    for event in events:
        ticker = event['series_ticker']
        url = f'https://api.elections.kalshi.com/trade-api/v2/markets?status=open&limit=1000&series_ticker={ticker}'
        markets = await get_paginated(url, 'markets')
        all_data.extend(markets)
        print(f"Fetched {len(markets)} markets, total: {len(all_data)}")

        # Insert into db
        for market in markets:
            cursor.execute('INSERT INTO kalshi_markets (ticker, close_time, yes_bid, yes_ask, no_bid, no_ask) VALUES (?, ?, ?, ?, ?, ?)',
                          (market['ticker'], market['close_time'], market['yes_bid'], market['yes_ask'], market['no_bid'], market['no_ask']))
        conn.commit()

    return all_data



async def main():
    # Events
    events_url = 'https://api.elections.kalshi.com/trade-api/v2/events?status=open'
    events = await get_paginated(events_url, 'events')
    print(f"Total markets found: {len(events)}")


    cursor.execute('SELECT COUNT(*) FROM kalshi_events')
    start_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM kalshi_events')
    conn.commit()
    added_count = cursor.fetchone()[0] - start_count

    print(f'Inserted {added_count} events')

    # Insert to db
    for event in events:
        cursor.execute('INSERT OR IGNORE INTO kalshi_events (ticker, title, category) VALUES (?, ?, ?)',
                      (event['series_ticker'], event['title'], event['category']))


    # Markets
    markets = await get_markets(events)
    print(markets[0])




asyncio.run(main())

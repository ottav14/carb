import requests
import time
import sqlite3
import asyncio

semaphore = asyncio.Semaphore(20)
conn = sqlite3.connect('/home/dom/projects/carb/backend/db/data.db')
cursor = conn.cursor()

async def api_call(url):
    async with semaphore:
        response = requests.get(url)
        data = response.json()
        await asyncio.sleep(0.1)
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
    total = 0
    for event in events:
        ticker = event[0]
        url = f'https://api.elections.kalshi.com/trade-api/v2/markets?status=open&limit=1000&series_ticker={ticker}'
        markets = await get_paginated(url, 'markets')
        total += len(markets)
        print(f"Fetched {len(markets)} markets, total: {total}")

        # Insert into db
        for market in markets:
            cursor.execute('INSERT INTO kalshi_markets (ticker, close_time, yes_bid, yes_ask, no_bid, no_ask) VALUES (?, ?, ?, ?, ?, ?)',
                          (market['ticker'], market['close_time'], market['yes_bid'], market['yes_ask'], market['no_bid'], market['no_ask']))
        conn.commit()




async def main():
    cursor.execute('SELECT * FROM kalshi_events')
    events = cursor.fetchall()
    await get_markets(events)

asyncio.run(main())

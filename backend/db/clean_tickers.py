import sqlite3

conn = sqlite3.connect('crypto.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM tickers;")
start_row_count = cursor.fetchone()[0]

cursor.execute("SELECT * FROM tickers;")
data = cursor.fetchall()
cursor.execute("""
    DELETE FROM tickers 
    WHERE id NOT IN (
        SELECT MAX(id)
        FROM tickers
        GROUP BY ticker
    );
""");

conn.commit();

cursor.execute("SELECT COUNT(*) FROM tickers;")
end_row_count = cursor.fetchone()[0]
deleted_row_count = start_row_count - end_row_count;
print(f'Deleted rows: {deleted_row_count}\nTickers remaining: {end_row_count}')

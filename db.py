import sqlite3

def init_db():
    conn = sqlite3.connect("shelflife.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            barcode TEXT,
            name TEXT,
            category TEXT,
            expiry_date TEXT,
            original_price REAL,
            current_price REAL,
            stock INTEGER,
            added_at TEXT)
    """)

    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect("shelflife.db")


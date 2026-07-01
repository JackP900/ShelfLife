import sqlite3
from datetime import datetime

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

def add_product(barcode, name, category, original_price, expiry_date, stock):
    conn = sqlite3.connect("shelflife.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO products (barcode, name, category, original_price, current_price, expiry_date, stock, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (barcode, name, category, original_price, original_price, expiry_date, stock, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()


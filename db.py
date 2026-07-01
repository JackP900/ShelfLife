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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_updates (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            old_price REAL,
            new_price REAL,
            reasoning TEXT,
            timestamp TEXT)
    """)

    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect("shelflife.db")
    conn.row_factory = sqlite3.Row
    return conn

def add_product(barcode, name, category, original_price, expiry_date, stock):
    conn = sqlite3.connect("shelflife.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO products (barcode, name, category, original_price, current_price, expiry_date, stock, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (barcode, name, category, original_price, original_price, expiry_date, stock, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def get_products_with_urgency():
    products = get_all_products()
    result = []
    
    for product in products:
        p = dict(product)

        expiry = datetime.strptime(p["expiry_date"], "%Y-%m-%d")
        days_left = (expiry - datetime.now()).days
        if days_left <= 2:
            p["urgency"] = "red"
        elif days_left <=5:
            p["urgency"] = "amber"
        else:
            p["urgency"] = "green"
            
        p["days_left"] = days_left
        result.append(p)
    
    return result

def get_get_product(product_id):
    conn = sqlite3.connect("shelflife.db")
    cursor = conn.cursor()
    cursor.execute("SELECT FROM products WHERE id = ?", (product_id))
    product = cursor.fetchone()
    conn.close()
    return product





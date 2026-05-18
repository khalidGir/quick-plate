import sqlite3
import json
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT NOT NULL,
        customer_username TEXT,
        address TEXT NOT NULL,
        items TEXT NOT NULL,
        extras TEXT,
        total_price REAL NOT NULL,
        status TEXT DEFAULT 'confirmed',
        claimed_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Menu table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        available BOOLEAN DEFAULT 1
    )
    ''')
    
    # Extras table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS extras (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    # Bot state table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bot_state (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    
    # Default bot state
    cursor.execute("INSERT OR IGNORE INTO bot_state (key, value) VALUES ('status', 'open')")
    
    # Initial Menu Data
    initial_menu = [
        ("Pizza Margherita", 8.0),
        ("Pepperoni Pizza", 10.0),
        ("Caesar Salad", 6.0),
        ("Garlic Bread", 3.0)
    ]
    cursor.executemany("INSERT OR IGNORE INTO menu (name, price) VALUES (?, ?)", initial_menu)
    
    # Initial Extras Data
    initial_extras = [
        ("Extra cheese", 1.50),
        ("Extra sauce", 0.50),
        ("Double meat", 3.0)
    ]
    cursor.executemany("INSERT OR IGNORE INTO extras (name, price) VALUES (?, ?)", initial_extras)
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
    print("Database initialized.")

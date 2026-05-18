import json
from database import get_db_connection
from datetime import datetime

def create_order(customer_id, customer_username, address, items, extras, total_price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (customer_id, customer_username, address, items, extras, total_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_id, customer_username, address, json.dumps(items), json.dumps(extras), total_price))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def update_order_status(order_id, status, claimed_by=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if claimed_by:
        cursor.execute('''
            UPDATE orders SET status = ?, claimed_by = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
        ''', (status, claimed_by, order_id))
    else:
        cursor.execute('''
            UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
        ''', (status, order_id))
    conn.commit()
    conn.close()

def get_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    return order

def get_active_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE status IN ('confirmed', 'preparing', 'on_the_way')")
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Today's stats
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT status, COUNT(*) FROM orders WHERE date(created_at) = ? GROUP BY status", (today,))
    stats = cursor.fetchall()
    conn.close()
    return stats

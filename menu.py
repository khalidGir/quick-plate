from database import get_db_connection

def get_active_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu WHERE available = 1")
    items = cursor.fetchall()
    conn.close()
    return items

def get_all_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()
    return items

def get_extras():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM extras")
    items = cursor.fetchall()
    conn.close()
    return items

def set_item_availability(name, available):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE menu SET available = ? WHERE name = ?", (available, name))
    conn.commit()
    conn.close()

def get_bot_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM bot_state WHERE key = 'status'")
    status = cursor.fetchone()[0]
    conn.close()
    return status

def set_bot_status(status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bot_state SET value = ? WHERE key = 'status'", (status,))
    conn.commit()
    conn.close()

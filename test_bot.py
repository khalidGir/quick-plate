import unittest
import os
import sqlite3
import json
from database import init_db, get_db_connection
from menu import get_active_menu, set_item_availability, get_bot_status, set_bot_status
from order_manager import create_order, update_order_status, get_order

class TestFoodBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a temporary test database
        if os.path.exists("test_food_bot.db"):
            os.remove("test_food_bot.db")
        
        # Patch the DB_PATH in modules to use test DB
        import config
        config.DB_PATH = "test_food_bot.db"
        
        init_db()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_food_bot.db"):
            os.remove("test_food_bot.db")

    def test_database_initialization(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn('orders', tables)
        self.assertIn('menu', tables)
        self.assertIn('bot_state', tables)
        conn.close()

    def test_menu_management(self):
        # Test getting active menu
        items = get_active_menu()
        self.assertGreater(len(items), 0)
        
        # Test hiding an item
        item_name = items[0]['name']
        set_item_availability(item_name, 0)
        
        new_items = get_active_menu()
        self.assertFalse(any(i['name'] == item_name for i in new_items))
        
        # Test showing it back
        set_item_availability(item_name, 1)
        self.assertTrue(any(i['name'] == item_name for i in get_active_menu()))

    def test_bot_status(self):
        self.assertEqual(get_bot_status(), 'open')
        set_bot_status('closed')
        self.assertEqual(get_bot_status(), 'closed')
        set_bot_status('open')

    def test_order_creation_and_status(self):
        customer_id = "12345"
        customer_name = "testuser"
        address = "123 Test St"
        items = [{'name': 'Pizza', 'qty': 1, 'price': 10.0}]
        extras = [{'name': 'Extra Cheese', 'price': 1.5}]
        total = 11.5
        
        order_id = create_order(customer_id, customer_name, address, items, extras, total)
        self.assertIsNotNone(order_id)
        
        order = get_order(order_id)
        self.assertEqual(order['status'], 'confirmed')
        self.assertEqual(order['address'], address)
        self.assertEqual(json.loads(order['items']), items)
        
        # Test status update
        update_order_status(order_id, 'preparing')
        order = get_order(order_id)
        self.assertEqual(order['status'], 'preparing')
        
        # Test claiming
        update_order_status(order_id, 'on_the_way', claimed_by='delivery_guy')
        order = get_order(order_id)
        self.assertEqual(order['status'], 'on_the_way')
        self.assertEqual(order['claimed_by'], 'delivery_guy')

if __name__ == '__main__':
    unittest.main()

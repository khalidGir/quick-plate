import os
from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
COOK_TELEGRAM_ID = int(os.getenv("COOK_TELEGRAM_ID", 0))
DELIVERY_TELEGRAM_ID = int(os.getenv("DELIVERY_TELEGRAM_ID", 0))

# Admin list for easier checks
ADMIN_IDS = [COOK_TELEGRAM_ID, DELIVERY_TELEGRAM_ID]

DB_PATH = "food_bot.db"

def is_user_admin(user_id):
    return user_id in ADMIN_IDS

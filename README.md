# Ju's Food Bot 🍕

A Telegram bot for a small food business with two human roles: Cook and Delivery Guy.

## Features
- Customer ordering flow with menu selection and extras.
- Multi-step address collection.
- Real-time notifications for Cook and Delivery Guy.
- Order status tracking: Confirmed -> Preparing -> On the Way -> Delivered.
- Admin commands to manage menu and bot status.

## Tech Stack
- Python 3.10+
- `python-telegram-bot` (v21.10)
- SQLite

## Setup Instructions

### 1. Create a Telegram Bot
- Find [@BotFather](https://t.me/botfather) on Telegram.
- Use `/newbot` to create your bot and get the **API Token**.

### 2. Get Admin IDs
- Use [@userinfobot](https://t.me/userinfobot) to get your Telegram User ID.
- You will need IDs for both the **Cook** and the **Delivery Guy**.

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
BOT_TOKEN=your_telegram_bot_token_here
COOK_TELEGRAM_ID=123456789
DELIVERY_TELEGRAM_ID=987654321
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Bot
```bash
python bot.py
```

## Deployment (Render.com)
1. Push this code to a GitHub repository.
2. Create a new "Web Service" on [Render.com](https://render.com).
3. Connect your repository.
4. Set the following:
   - **Environment**: Python
   - **Start Command**: `python bot.py`
5. Add your `.env` variables in the "Environment" tab of Render's dashboard.
6. Render's free tier is usually sufficient for low-traffic bots. Note: SQLite data will be lost if the service restarts unless you use a persistent disk (which Render provides).

## Admin Commands
- `/hide [item_name]` - Temporarily hide an item.
- `/show [item_name]` - Show a hidden item.
- `/close` - Stop accepting new orders.
- `/open` - Start accepting orders.
- `/orders` - List active orders.
- `/stats` - Show today's order statistics.

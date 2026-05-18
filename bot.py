import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from database import init_db
from customer_handlers import start, show_menu, order_conv_handler
from admin_handlers import (
    hide_item, show_item, close_bot, open_bot, 
    list_orders, show_stats, admin_button_click, admin_panel
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Initialize DB
    init_db()

    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in environment variables.")
        return

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Public commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))
    application.add_handler(order_conv_handler)

    # Admin commands
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("hide", hide_item))
    application.add_handler(CommandHandler("show", show_item))
    application.add_handler(CommandHandler("close", close_bot))
    application.add_handler(CommandHandler("open", open_bot))
    application.add_handler(CommandHandler("orders", list_orders))
    application.add_handler(CommandHandler("stats", show_stats))
    
    # Button clicks
    # Map the "Admin Panel" button from start command directly to admin_panel function
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel_open$"))
    application.add_handler(CallbackQueryHandler(admin_button_click, pattern="^admin_"))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()

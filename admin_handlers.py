from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from menu import set_item_availability, set_bot_status, get_all_menu, get_bot_status
from order_manager import update_order_status, get_order, get_active_orders, get_stats
from config import ADMIN_IDS, COOK_TELEGRAM_ID, DELIVERY_TELEGRAM_ID, is_user_admin

async def hide_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("Usage: /hide [item_name]")
        return
    item_name = " ".join(context.args)
    set_item_availability(item_name, 0)
    await update.message.reply_text(f"Item '{item_name}' hidden from menu.")

async def show_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("Usage: /show [item_name]")
        return
    item_name = " ".join(context.args)
    set_item_availability(item_name, 1)
    await update.message.reply_text(f"Item '{item_name}' now visible.")

async def close_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id): return
    set_bot_status('closed')
    await update.message.reply_text("Bot is now CLOSED. No new orders accepted.")

async def open_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id): return
    set_bot_status('open')
    await update.message.reply_text("Bot is now OPEN. Accepting orders!")

async def list_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id): return
    orders = get_active_orders()
    
    # Determine where to send the reply (message or callback query)
    target = update.message if update.message else update.callback_query.message

    if not orders:
        await target.reply_text("No active orders.")
        return
    
    text = "📋 *Active Orders*\n\n"
    for o in orders:
        text += f"#{o['order_id']} - {o['status']} - {o['customer_username']}\n"
    
    await target.reply_text(text, parse_mode='Markdown')

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id): return
    stats = get_stats()
    
    target = update.message if update.message else update.callback_query.message

    if not stats:
        await target.reply_text("No orders today yet.")
        return
    
    text = "📊 *Today's Stats*\n\n"
    total = 0
    for status, count in stats:
        text += f"• {status.capitalize()}: {count}\n"
        total += count
    text += f"\n*Total Orders: {total}*"
    await target.reply_text(text, parse_mode='Markdown')

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id):
        # Handle case where this is called from a button click
        target = update.message if update.message else update.callback_query.message
        await target.reply_text("Unauthorized. This area is for staff only.")
        return

    status = get_bot_status()
    status_icon = "🟢 OPEN" if status == 'open' else "🔴 CLOSED"

    keyboard = [
        [InlineKeyboardButton("📋 Active Orders", callback_data="admin_list_orders")],
        [InlineKeyboardButton("📊 Today's Stats", callback_data="admin_view_stats")],
        [InlineKeyboardButton("🚪 Close Shop", callback_data="admin_close_shop"), 
         InlineKeyboardButton("🟢 Open Shop", callback_data="admin_open_shop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    panel_text = f"🛠 *Admin Control Panel*\nStatus: {status_icon}\n\nSelect an action:"
    
    if update.message:
        await update.message.reply_text(panel_text, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(panel_text, parse_mode='Markdown', reply_markup=reply_markup)

async def admin_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    if not is_user_admin(user_id):
        await query.answer("Unauthorized", show_alert=True)
        return
    
    data = query.data
    
    # Handle Panel Buttons
    if data == "admin_list_orders":
        await query.answer()
        await list_orders(update, context)
        return
    elif data == "admin_view_stats":
        await query.answer()
        await show_stats(update, context)
        return
    elif data == "admin_close_shop":
        set_bot_status('closed')
        await query.answer("Shop Closed", show_alert=False)
        await admin_panel(update, context) # Refresh the panel
        return
    elif data == "admin_open_shop":
        set_bot_status('open')
        await query.answer("Shop Open", show_alert=False)
        await admin_panel(update, context) # Refresh the panel
        return

    # Handle Order Ticket Buttons (preparing, claim, done)
    order_id_parts = data.split('_')
    if len(order_id_parts) < 3: return
    order_id = int(order_id_parts[-1])
    order = get_order(order_id)
    
    if not order:
        await query.answer("Order not found.")
        return

    if "preparing" in data:
        update_order_status(order_id, 'preparing')
        await query.answer("Order marked as preparing.")
        # Notify customer
        await context.bot.send_message(chat_id=order['customer_id'], text=f"🍳 Your order #{order_id} is being prepared!")
        # Notify Delivery Guy
        if DELIVERY_TELEGRAM_ID:
            await context.bot.send_message(chat_id=DELIVERY_TELEGRAM_ID, text=f"🍳 Order #{order_id} is being prepared by the cook.")
        
    elif "claim" in data:
        if user_id != DELIVERY_TELEGRAM_ID:
            await query.answer("Only the Delivery Guy can claim orders!", show_alert=True)
            return
        
        if order['status'] == 'on_the_way':
            await query.answer("Order already claimed!")
            return
            
        username = update.effective_user.username or update.effective_user.first_name
        update_order_status(order_id, 'on_the_way', claimed_by=username)
        await query.answer("Order claimed!")
        
        # Notify customer
        await context.bot.send_message(chat_id=order['customer_id'], text=f"🚚 Your order #{order_id} is on the way! Claimed by @{username}.")
        # Notify Cook
        if COOK_TELEGRAM_ID:
            await context.bot.send_message(chat_id=COOK_TELEGRAM_ID, text=f"🚚 Order #{order_id} claimed by @{username} — on the way!")

    elif "done" in data:
        update_order_status(order_id, 'delivered')
        await query.answer("Order marked as delivered.")
        # Notify customer
        await context.bot.send_message(chat_id=order['customer_id'], text=f"✅ Your order #{order_id} has been delivered. Enjoy!")
        # Notify both admins
        for admin_id in ADMIN_IDS:
            if admin_id:
                await context.bot.send_message(chat_id=admin_id, text=f"✅ Order #{order_id} delivered!")

    # Update the admin message with new status
    new_text = query.message.text.split("Status:")[0] + f"Status: {order['status'].upper()}"
    if order['claimed_by']:
        new_text += f"\nClaimed by: @{order['claimed_by']}"
    
    # Update buttons
    keyboard = []
    if order['status'] == 'confirmed':
        keyboard.append([InlineKeyboardButton("🍳 Mark Preparing", callback_data=f"admin_preparing_{order_id}")])
    if order['status'] in ['confirmed', 'preparing']:
        keyboard.append([InlineKeyboardButton("🚚 Claim & Deliver", callback_data=f"admin_claim_{order_id}")])
    if order['status'] == 'on_the_way':
        keyboard.append([InlineKeyboardButton("✅ Mark Delivered", callback_data=f"admin_done_{order_id}")])
    
    await query.edit_message_text(text=new_text, reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

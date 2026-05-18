import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from menu import get_active_menu, get_extras, get_bot_status
from order_manager import create_order
from config import COOK_TELEGRAM_ID, DELIVERY_TELEGRAM_ID, is_user_admin

# Conversation states
SELECT_ITEM, SELECT_QUANTITY, SELECT_EXTRAS, ENTER_ADDRESS, CONFIRM_ORDER = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    status = get_bot_status()
    
    is_admin = is_user_admin(user_id)
    
    if status == 'closed' and not is_admin:
        await update.message.reply_text("Bot is closed. Come back tomorrow.")
        return ConversationHandler.END

    welcome_text = "Welcome to Ju's Food Bot! 🍕\n\nUse /order to start a new order or /menu to see what's cooking."
    
    keyboard = []
    if is_admin:
        welcome_text += "\n\n🛠 *Staff Member Detected*\nYou can use /admin to open the control panel."
        keyboard.append([InlineKeyboardButton("🛠 Admin Panel", callback_data="admin_panel_open")])
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

# Helper for admin button in start
async def start_admin_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This will be handled in bot.py to avoid circular import
    pass

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_active_menu()
    if not items:
        await update.message.reply_text("The menu is currently empty.")
        return

    menu_text = "📋 *Our Menu*\n\n"
    for item in items:
        menu_text += f"• {item['name']} — ${item['price']:.2f}\n"
    
    await update.message.reply_text(menu_text, parse_mode='Markdown')

async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = get_bot_status()
    if status == 'closed':
        await update.message.reply_text("Bot is closed. Come back tomorrow.")
        return ConversationHandler.END

    # Reset order data for a fresh start
    context.user_data['order'] = {}

    items = get_active_menu()
    if not items:
        await update.message.reply_text("Sorry, we are sold out of everything!")
        return ConversationHandler.END

    keyboard = []
    for item in items:
        keyboard.append([InlineKeyboardButton(f"{item['name']} - ${item['price']}", callback_data=f"item_{item['id']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an item from the menu:", reply_markup=reply_markup)
    return SELECT_ITEM

async def item_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[1])
    # Fetch item details from DB (simulated here for brevity, better to use item_id)
    items = get_active_menu()
    selected_item = next((i for i in items if i['id'] == item_id), None)
    
    if not selected_item:
        await query.edit_message_text("Item not found. Please try again.")
        return SELECT_ITEM

    context.user_data['order'] = {
        'item': selected_item,
        'quantity': 1,
        'extras': []
    }

    keyboard = [[InlineKeyboardButton(str(i), callback_data=f"qty_{i}") for i in range(1, 6)],
                [InlineKeyboardButton(str(i), callback_data=f"qty_{i}") for i in range(6, 11)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(f"How many {selected_item['name']} would you like?", reply_markup=reply_markup)
    return SELECT_QUANTITY

async def quantity_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    qty = int(query.data.split('_')[1])
    context.user_data['order']['quantity'] = qty
    
    extras = get_extras()
    keyboard = []
    for extra in extras:
        keyboard.append([InlineKeyboardButton(f"Add {extra['name']} (+${extra['price']})", callback_data=f"extra_{extra['id']}")])
    keyboard.append([InlineKeyboardButton("Done with extras", callback_data="extras_done")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Would you like to add any extras?", reply_markup=reply_markup)
    return SELECT_EXTRAS

async def extra_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "extras_done":
        await query.edit_message_text("Please type your delivery address:")
        return ENTER_ADDRESS
    
    extra_id = int(query.data.split('_')[1])
    extras = get_extras()
    selected_extra = next((e for e in extras if e['id'] == extra_id), None)
    
    if selected_extra:
        if 'extras' not in context.user_data['order']:
            context.user_data['order']['extras'] = []
        context.user_data['order']['extras'].append(selected_extra)
        
        # Build the extras list for the message
        added_extras = ", ".join([e['name'] for e in context.user_data['order']['extras']])
        
        # Re-send the keyboard so they can add more or finish
        keyboard = []
        for extra in extras:
            keyboard.append([InlineKeyboardButton(f"Add {extra['name']} (+${extra['price']})", callback_data=f"extra_{extra['id']}")])
        keyboard.append([InlineKeyboardButton("Done with extras", callback_data="extras_done")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"Current Extras: {added_extras}\n\nWould you like to add more?", 
            reply_markup=reply_markup
        )
    
    return SELECT_EXTRAS

async def address_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text
    context.user_data['order']['address'] = address
    
    order = context.user_data['order']
    item = order['item']
    qty = order['quantity']
    extras = order['extras']
    
    total = item['price'] * qty
    extras_text = ""
    for extra in extras:
        total += extra['price']
        extras_text += f"- {extra['name']} (+${extra['price']})\n"
    
    summary = (
        f"🛒 *Order Summary*\n\n"
        f"Item: {item['name']} x{qty} = ${item['price']*qty:.2f}\n"
        f"Extras:\n{extras_text if extras_text else 'None'}\n"
        f"Address: {address}\n"
        f"*Total: ${total:.2f}*\n\n"
        f"Confirm order?"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm_yes")],
        [InlineKeyboardButton("❌ Cancel", callback_data="confirm_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.user_data['order']['total'] = total
    await update.message.reply_text(summary, parse_mode='Markdown', reply_markup=reply_markup)
    return CONFIRM_ORDER

async def order_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm_no":
        await query.edit_message_text("Order cancelled. Use /order to start again.")
        return ConversationHandler.END
    
    order = context.user_data['order']
    customer = update.effective_user
    
    order_id = create_order(
        customer_id=customer.id,
        customer_username=customer.username or customer.first_name,
        address=order['address'],
        items=[{'name': order['item']['name'], 'qty': order['quantity'], 'price': order['item']['price']}],
        extras=[{'name': e['name'], 'price': e['price']} for e in order['extras']],
        total_price=order['total']
    )
    
    await query.edit_message_text(f"Order confirmed! Your Order ID is #{order_id}. We'll notify you when it's preparing.")
    
    # Notify Cook and Delivery Guy
    notification = (
        f"🍽 *NEW ORDER #{order_id}*\n"
        f"Customer: @{customer.username or customer.first_name} (ID: {customer.id})\n"
        f"Items: {order['item']['name']} x{order['quantity']}\n"
        f"Extras: {', '.join([e['name'] for e in order['extras']]) if order['extras'] else 'None'}\n"
        f"Address: {order['address']}\n"
        f"Total: ${order['total']:.2f}\n"
        f"Status: CONFIRMED"
    )
    
    admin_keyboard = [
        [InlineKeyboardButton("🍳 Mark Preparing", callback_data=f"admin_preparing_{order_id}")],
        [InlineKeyboardButton("🚚 Claim & Deliver", callback_data=f"admin_claim_{order_id}")]
    ]
    admin_markup = InlineKeyboardMarkup(admin_keyboard)
    
    for admin_id in [COOK_TELEGRAM_ID, DELIVERY_TELEGRAM_ID]:
        if admin_id:
            try:
                await context.bot.send_message(chat_id=admin_id, text=notification, parse_mode='Markdown', reply_markup=admin_markup)
            except Exception as e:
                print(f"Error notifying admin {admin_id}: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Order cancelled.")
    return ConversationHandler.END

order_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("order", start_order)],
    states={
        SELECT_ITEM: [CallbackQueryHandler(item_selected, pattern="^item_")],
        SELECT_QUANTITY: [CallbackQueryHandler(quantity_selected, pattern="^qty_")],
        SELECT_EXTRAS: [CallbackQueryHandler(extra_selected, pattern="^extra_|extras_done")],
        ENTER_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address_entered)],
        CONFIRM_ORDER: [CallbackQueryHandler(order_confirmed, pattern="^confirm_")],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

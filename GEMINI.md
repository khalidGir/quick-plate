# Ju's Food Bot (QuickPlate) 🍕

Ju's Food Bot is a Telegram-based ordering system designed for small food businesses. It facilitates a smooth workflow between customers, cooks, and delivery personnel, featuring real-time notifications and order status tracking.

## Architecture & Core Components

The project is built using a modular Python architecture with a SQLite backend:

-   **`bot.py`**: The main entry point. It initializes the database, configures the Telegram `Application`, and registers command/callback handlers.
-   **`customer_handlers.py`**: Manages the customer-facing side of the bot, including a multi-step `ConversationHandler` for the ordering process (item selection, quantity, extras, address, and confirmation).
-   **`admin_handlers.py`**: Contains logic for staff members (Cooks and Delivery Guys). It handles administrative commands like `/hide`, `/show`, `/close`, `/open`, and `/stats`, as well as interactive button clicks to update order statuses.
-   **`database.py`**: Handles SQLite database initialization and provides a connection factory. The schema includes tables for `orders`, `menu`, `extras`, and `bot_state`.
-   **`menu.py`**: Provides an abstraction layer for menu management (fetching active items, toggling availability).
-   **`order_manager.py`**: Manages order persistence and lifecycle (creation, status updates, statistics).
-   **`config.py`**: Centralizes configuration, loading environment variables for the bot token and admin IDs.

## Technology Stack

-   **Language**: Python 3.10+
-   **Framework**: `python-telegram-bot` (v21.10)
-   **Database**: SQLite
-   **Environment Management**: `python-dotenv`

## Getting Started

### Prerequisites

-   Python 3.10 or higher.
-   A Telegram Bot token from [@BotFather](https://t.me/botfather).
-   Telegram User IDs for the Cook and Delivery Guy (use [@userinfobot](https://t.me/userinfobot)).

### Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables by creating a `.env` file (see `.env.example`):
    ```env
    BOT_TOKEN=your_token_here
    COOK_TELEGRAM_ID=123456789
    DELIVERY_TELEGRAM_ID=987654321
    ```

### Running the Bot

Start the bot locally with:
```bash
python bot.py
```

### Running Tests

Execute the unit tests to verify the database and logic:
```bash
python test_bot.py
```

## Development Conventions

-   **Modular Handlers**: Keep customer and admin logic separated in their respective `_handlers.py` files.
-   **Conversation Flow**: Use `ConversationHandler` for complex multi-step interactions.
-   **Database Access**: Always use `get_db_connection()` from `database.py` to interact with the SQLite database.
-   **Environment Variables**: All sensitive configuration should be stored in `.env` and accessed via `config.py`.
-   **Async/Await**: The project strictly uses `async/await` patterns as required by `python-telegram-bot` v20+.

## Deployment

The project is optimized for deployment on platforms like Render.com.
-   **Start Command**: `python bot.py`
-   **Persistence**: Note that SQLite requires a persistent disk on Render to maintain data across restarts.

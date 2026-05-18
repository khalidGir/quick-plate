# 🚀 Demo Guide: Ju's Food Bot

Follow these steps to set up the bot and give a "wow" demonstration to your client (Ju).

---

## 🛠 Phase 1: Preparation (Do this before the demo)

1.  **Get a Bot Token**:
    *   Message [@BotFather](https://t.me/botfather) on Telegram.
    *   `/newbot` -> Name it "Ju's QuickPlate" -> Save the **API Token**.
2.  **Get Your Telegram ID**:
    *   Message [@userinfobot](https://t.me/userinfobot) to get your personal ID (a 9-10 digit number).
3.  **Configure the Bot**:
    *   Create a `.env` file in the project folder.
    *   Put your ID in BOTH `COOK_TELEGRAM_ID` and `DELIVERY_TELEGRAM_ID` for testing.
    ```env
    BOT_TOKEN=your_token_here
    COOK_TELEGRAM_ID=your_id
    DELIVERY_TELEGRAM_ID=your_id
    ```
4.  **Install & Run**:
    ```bash
    pip install -r requirements.txt
    python bot.py
    ```

---

## 🎭 Phase 2: The Demo Script (The "Happy Path")

### Step 1: The Customer Experience
1.  Open your Telegram bot and click **START**.
2.  Type `/menu` to show the beautiful text-based menu.
3.  Type `/order` to start the flow:
    *   **Select Item**: Click "Pepperoni Pizza".
    *   **Select Qty**: Click "2".
    *   **Add Extras**: Click "Extra Cheese" -> Then click "Done with extras".
    *   **Address**: Type "123 Magic Lane, near the blue gate".
    *   **Confirm**: Look at the summary and click "✅ Confirm".

### Step 2: The Cook's Role
*   You will receive a notification instantly in the **same chat** (since you are the admin).
*   *Explain to Ju:* "The Cook sees this immediately. They know what to make and where it's going."
*   Click **🍳 Mark Preparing**.
*   *Observe:* You'll get a customer message saying "Your order is being prepared!"

### Step 3: The Delivery Guy's Role
*   *Explain to Ju:* "Now the Delivery Guy sees the order is ready for pickup."
*   Click **🚚 Claim & Deliver**.
*   *Observe:* The status updates to "ON_THE_WAY" and the customer is notified.
*   Click **✅ Mark Delivered**.
*   *Observe:* Both roles and the customer get the final completion message.

---

## 🛠 Phase 3: Showing Admin Power
1.  **Hide an Item**: Type `/hide Caesar Salad`. Then type `/menu` to show it's gone.
2.  **Close Shop**: Type `/close`. Try to `/order` again to show the "Closed" message.
3.  **Stats**: Type `/stats` to show the client how they can track daily sales.

---

## 💡 Pro-Tips for a Great Demo
*   **Two Phones**: If possible, have a friend or use a second Telegram account to act as the "Customer" while you handle the "Admin" buttons on your phone.
*   **Explain the "Why"**: Emphasize that there are **no fees**, **no complex maps**, and it works on **any phone** with Telegram.
*   **Deployment**: Tell Ju: "I can host this on Render for free, so your monthly cost is $0."

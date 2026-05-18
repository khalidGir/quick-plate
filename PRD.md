# Product Requirements Document (PRD): QuickPlate (Ju's Food Bot)

**Version:** 1.0  
**Status:** In Development / Testing  
**Lead Developer:** Gemini CLI Agent  
**Stakeholders:** Ju (Business Owner), Cook, Delivery Personnel, Customers  

---

## 1. Executive Summary
**QuickPlate** is a lightweight, Telegram-native ordering system designed for small-scale food businesses (cloud kitchens, local cafes). It automates the intake of orders, coordinates between kitchen and delivery staff, and provides customers with real-time status updates without the overhead of a heavy mobile app or website.

---

## 2. Problem Statement
Small food businesses often manage orders via fragmented WhatsApp messages or phone calls. This leads to:
- **Mismanaged orders:** Difficulty tracking what is "being cooked" vs "out for delivery."
- **Customer Anxiety:** Customers don't know the status of their food.
- **Manual Overhead:** Staff must manually text customers at every stage.

---

## 3. Target Audience
1.  **Customers:** Users looking for a fast, friction-less way to order food via Telegram.
2.  **The Cook:** Staff responsible for food preparation who needs to see new orders and signal when they are ready.
3.  **The Delivery Guy:** Staff responsible for logistics who needs to claim orders and navigate to addresses.
4.  **The Admin (Ju):** The owner who manages the menu and monitors daily performance.

---

## 4. Functional Requirements

### 4.1 Customer Experience (The Bot Interface)
- **Menu Discovery:** Users can view a formatted list of items and prices using `/menu`.
- **Interactive Ordering:** A guided 5-step conversation flow via `/order`:
    1. **Selection:** Pick an item from an inline button list.
    2. **Quantity:** Select 1–10 units via a button grid.
    3. **Customization:** Add optional "Extras" (e.g., extra cheese) with real-time price calculation.
    4. **Logistics:** Provide delivery address via text input.
    5. **Confirmation:** Final review of the "Order Receipt" before submission.
- **Automated Notifications:** Customers receive push messages when:
    - Order is confirmed.
    - Food starts being prepared (Cook signal).
    - Food is out for delivery (Delivery signal).
    - Food is delivered.

### 4.2 Staff Experience (Admin Handlers)
- **Centralized Notifications:** Both the Cook and Delivery Guy receive a "New Order" ticket with all details.
- **One-Click Updates:** Inline buttons on the order ticket to change state:
    - `[🍳 Mark Preparing]`
    - `[🚚 Claim & Deliver]`
    - `[✅ Mark Delivered]`
- **Role-Based Permissions:** Only users with IDs in the `.env` configuration can access admin buttons or commands.

### 4.3 Management & Operations
- **Menu Management:** Admins can toggle item visibility using `/hide [item]` or `/show [item]`.
- **Operating Hours:** Admins can toggle the bot's availability using `/open` and `/close`.
- **Reporting:** Daily statistics via `/stats` (Total orders, breakdown by status).

---

## 5. Technical Requirements

### 5.1 Tech Stack
- **Language:** Python 3.10+
- **Framework:** `python-telegram-bot` (v21.10) using asynchronous patterns.
- **Database:** SQLite (local persistence) for orders, menu items, and bot state.
- **Configuration:** `python-dotenv` for secure management of `BOT_TOKEN` and staff IDs.

### 5.2 Data Schema
- **Orders:** ID, customer info, serialized item list, total price, status, timestamps, and `claimed_by` fields.
- **Menu/Extras:** ID, name, price, availability flag.
- **Bot State:** Persistent storage for 'open'/'closed' status.

---

## 6. User Flows

### 6.1 The "Happy Path" Ordering Flow
1. Customer `/order` -> Bot shows Menu Buttons.
2. Customer clicks **"Pepperoni Pizza"** -> Bot shows Quantity Buttons.
3. Customer clicks **"2"** -> Bot shows Extras (Extra Cheese, etc.).
4. Customer clicks **"Done"** -> Bot asks for Address.
5. Customer types **"123 Maple St"** -> Bot shows Summary.
6. Customer clicks **"✅ Confirm"**.
7. **Internal:** Ticket sent to Cook/Delivery.

---

## 7. UX/UI Principles
- **Minimal Text Entry:** Use inline buttons whenever possible (Selection, Quantity, Extras) to reduce user error.
- **State Persistence:** Ensure the bot handles "stale" conversations by resetting user data on every new `/order` call.
- **Feedback Loops:** Use `query.answer()` in Telegram to provide "Toast" notifications (short popup alerts) for every button click.

---

## 8. Success Metrics
- **Response Time:** Time from "Order Confirmed" to "Mark Preparing" (Kitchen Efficiency).
- **Delivery Time:** Time from "Claimed" to "Delivered" (Logistics Efficiency).
- **Daily Volume:** Number of successful orders completed vs cancelled.

---

## 9. Future Considerations (Phase 2)
- **Payment Integration:** Support for Telegram Payments (Stripe/Crypto).
- **Multi-Item Cart:** Allow users to add different items (e.g., 1 Pizza AND 1 Salad) in a single order.
- **Location Sharing:** Use Telegram's live location feature instead of manual address typing.
- **Admin Dashboard:** A web-based view of the `food_bot.db` for the owner.

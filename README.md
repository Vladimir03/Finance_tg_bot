# Finance Telegram Bot

This repository contains a simple Telegram bot that records your incomes and expenses in a local CSV file.

## Algorithm Overview

1. **Create a bot in Telegram** using [BotFather](https://core.telegram.org/bots#botfather) and obtain the bot token.
2. **Configure environment variables** for the bot. You can copy `.env.example`
   to `.env` and fill in your values. The bot will automatically load this file
   on startup:
   - `TELEGRAM_TOKEN` – token received from BotFather.
3. Install dependencies with `pip install -r requirements.txt`.
4. **Run the bot** using `python bot.py`.
5. Use `/start` to show buttons for adding income, adding expense, or viewing
   the monthly summary. You can also use the `/help` command to see available
   commands. The `/add_income` and `/add_expense` commands accept an amount and
   description, while `/summary` displays totals for the current month.

Transactions are saved to `transactions.csv` in the repository root.

# Finance Telegram Bot

This repository contains a simple Telegram bot that records your incomes and expenses and saves them to a Google Sheet.

## Algorithm Overview

1. **Create a bot in Telegram** using [BotFather](https://core.telegram.org/bots#botfather) and obtain the bot token.
2. **Set up Google Sheets API**:
   - Create a Google Cloud project and enable the Google Sheets API.
   - Create a service account and download the JSON credentials file.
   - Share the target spreadsheet with the service account email.
3. **Configure environment variables** for the bot:
   - `TELEGRAM_TOKEN` – token received from BotFather.
   - `GOOGLE_CREDENTIALS_JSON` – path to the service account JSON file.
   - `SPREADSHEET_KEY` – ID of the Google spreadsheet (the part between
     `/d/` and `/edit` in the spreadsheet URL).
4. Install dependencies with `pip install -r requirements.txt`.
5. **Run the bot** using `python bot.py`.
6. Use the `/help` command to see available actions. Commands `/add_income` and
   `/add_expense` accept an amount and description to log transactions.

Transactions are appended to the `Transactions` sheet in the specified spreadsheet.

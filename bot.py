import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import gspread
from datetime import datetime

# Load tokens from environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GOOGLE_CREDENTIALS_JSON = os.environ.get('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_KEY = os.environ.get('SPREADSHEET_KEY')

# Initialize Google Sheets client
if GOOGLE_CREDENTIALS_JSON and SPREADSHEET_KEY:
    gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_JSON)
    sh = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = sh.worksheet('Transactions')
else:
    worksheet = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome! Use /add_income or /add_expense to log transactions.')

async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Usage: /add_income amount description')
        return
    amount = context.args[0]
    description = ' '.join(context.args[1:])
    _log_transaction('income', amount, description)
    await update.message.reply_text('Income recorded.')

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Usage: /add_expense amount description')
        return
    amount = context.args[0]
    description = ' '.join(context.args[1:])
    _log_transaction('expense', amount, description)
    await update.message.reply_text('Expense recorded.')


def _log_transaction(tx_type: str, amount: str, description: str):
    if worksheet:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        worksheet.append_row([timestamp, tx_type, amount, description])


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('add_income', add_income))
    app.add_handler(CommandHandler('add_expense', add_expense))

    app.run_polling()


if __name__ == '__main__':
    main()

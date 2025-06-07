import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import gspread
from datetime import datetime

# Load environment variables from a .env file if present
load_dotenv()

# Load tokens from environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
# GOOGLE_CREDENTIALS_JSON = os.environ.get('GOOGLE_CREDENTIALS_JSON')
# SPREADSHEET_KEY = os.environ.get('SPREADSHEET_KEY')

if not TELEGRAM_TOKEN:
    raise RuntimeError('TELEGRAM_TOKEN environment variable is required')

# Initialize Google Sheets client
# if GOOGLE_CREDENTIALS_JSON and SPREADSHEET_KEY:
  #  try:
   #     gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_JSON)
    #except Exception as e:
     #   raise RuntimeError(f'Failed to load Google credentials: {e}')

    #try:
     #   sh = gc.open_by_key(SPREADSHEET_KEY)
      #  worksheet = sh.worksheet('Transactions')
    #except gspread.exceptions.WorksheetNotFound:
     #   raise RuntimeError("'Transactions' worksheet not found in the spreadsheet")
    #except Exception as e:
     #   raise RuntimeError(f'Failed to access spreadsheet: {e}')
#else:
 #   worksheet = None
  #  print('Google Sheets credentials are missing; transactions will not be saved')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome! Use /add_income or /add_expense to log transactions.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Commands:\n'
        '/add_income amount description - log income\n'
        '/add_expense amount description - log expense')

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


#def _log_transaction(tx_type: str, amount: str, description: str):
 #   if worksheet:
  #      timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
   #     worksheet.append_row([timestamp, tx_type, amount, description])


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_income', add_income))
    app.add_handler(CommandHandler('add_expense', add_expense))

    app.run_polling()


if __name__ == '__main__':
    main()

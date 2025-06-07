import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from datetime import datetime
import csv

# Load environment variables from a .env file if present
load_dotenv()

# Load tokens from environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CSV_FILE = 'transactions.csv'

# conversation states
AMOUNT, DESCRIPTION = range(2)

if not TELEGRAM_TOKEN:
    raise RuntimeError('TELEGRAM_TOKEN environment variable is required')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Add income", callback_data="income"),
            InlineKeyboardButton("Add expense", callback_data="expense"),
        ],
        [InlineKeyboardButton("Monthly summary", callback_data="summary")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Choose an option:", reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Commands:\n'
        '/add_income amount description - log income\n'
        '/add_expense amount description - log expense\n'
        '/summary - show monthly totals')

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


async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['tx_type'] = query.data
    await query.message.reply_text('Enter amount:')
    return AMOUNT


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['amount'] = update.message.text
    await update.message.reply_text('Enter description:')
    return DESCRIPTION


async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tx_type = context.user_data.get('tx_type')
    amount = context.user_data.get('amount')
    description = update.message.text
    _log_transaction(tx_type, amount, description)
    await update.message.reply_text(f'{tx_type.capitalize()} recorded.')
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Cancelled.')
    return ConversationHandler.END


def _calculate_monthly_totals():
    income_total = 0.0
    expense_total = 0.0
    now = datetime.utcnow()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                timestamp, tx_type, amount, desc = row
                ts = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                if ts.year == now.year and ts.month == now.month:
                    if tx_type == 'income':
                        income_total += float(amount)
                    elif tx_type == 'expense':
                        expense_total += float(amount)
    return income_total, expense_total


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    income_total, expense_total = _calculate_monthly_totals()
    month_str = datetime.utcnow().strftime('%Y-%m')
    await update.message.reply_text(
        f"Totals for {month_str}\n"
        f"Income: {income_total}\n"
        f"Expense: {expense_total}"
    )


def _log_transaction(tx_type: str, amount: str, description: str):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, tx_type, amount, description])


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add, pattern='^(income|expense)$')],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_income', add_income))
    app.add_handler(CommandHandler('add_expense', add_expense))
    app.add_handler(CommandHandler('summary', summary))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(summary, pattern='^summary$'))

    app.run_polling()


if __name__ == '__main__':
    main()

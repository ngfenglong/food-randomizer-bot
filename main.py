import os
import telegram.ext

TOKEN = str(os.getenv("TELEGRAM_ACCESS_KEY"))
# with open('token.txt', 'r') as f:
#     TOKEN = f.read()

def start(update, context):
    update.message.reply_text("Hello! Welcome to Novena Lunch Generator")

def help(update, context):
    update.message.reply_text("""
    The following commands are available: 

    /start -> Welcome Message
    /help -> Help Messagegit init
    /generate -> Generate food suggestion
    """)

def generate(update, context):
    update.message.reply_text("Generating....")

updater  = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("generate", generate))

updater.start_polling()
updater.idle()

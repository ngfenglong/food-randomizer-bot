import telebot
from config import TOKEN
from handlers import start, help, generatePlace, handle_unrecognized_command

bot = telebot.TeleBot(TOKEN)

# Public Handlers
bot.register_message_handler(start, commands=['start', 'hello'])
bot.register_message_handler(help, commands=['help'])
bot.register_message_handler(generatePlace, commands=['generate'])
bot.register_message_handler(handle_unrecognized_command, func=lambda m: True)

bot.infinity_polling()
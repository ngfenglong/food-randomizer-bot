# bot/__init__.py
from telebot import TeleBot
from config import settings

# Initialize the bot
bot = TeleBot(settings.TOKEN)

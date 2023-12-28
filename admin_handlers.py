from telebot import types
from config import ADMIN_USER_IDS, TOKEN
import telebot
from utils import fetch_all_places, format_places, fetch_all_categories, fetch_all_locations, add_place_api

# Initialize the bot instance
from bot_instance import bot

def is_user_admin(user_id):
    return user_id in ADMIN_USER_IDS


def admin_menu(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, "You are not authorized to access admin functions.")
        return

    menu_message = "Admin Menu:\n" \
                   "/view_places - View all places\n" \
                   "/add_place - Add a new place\n" \
                   "/delete_place - Delete a place\n"
    bot.send_message(message.chat.id, menu_message)

def view_places(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, "You are not authorized to access this function.")
        return

    places = fetch_all_places()  
    formatted_response = format_places(places)  
    bot.send_message(message.chat.id, formatted_response)

def add_place(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, "You are not authorized to access this function.")
        return

    # Start the process by asking for a category
    bot.send_message(message.chat.id, "Please select a category:", reply_markup=get_categories_markup())

def get_categories_markup():
    categories = fetch_all_categories()  
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        markup.add(types.InlineKeyboardButton(category['category_name'], callback_data=f"cat_{category['id']}"))
    return markup


def category_callback(call):
    category_id = call.data.split('_')[1]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Please select a location:", reply_markup=get_locations_markup(category_id))


def get_locations_markup(category_id):
    locations = fetch_all_locations()  # Implement this to fetch locations from your API
    markup = types.InlineKeyboardMarkup()
    for location in locations:
        markup.add(types.InlineKeyboardButton(location['location_name'], callback_data=f"loc_{location['id']}_{category_id}"))
    return markup

def location_callback(call):
    location_id, category_id = call.data.split('_')[1:]
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "Please send the remaining place details in this format:\n"
                                                 "Name, Description, IsHalal (True/False), IsVegetarian (True/False)")
    bot.register_next_step_handler(msg, process_place_details, category_id, location_id)

def process_place_details(message, category_id, location_id):
    try:
        name, description, is_halal, is_vegetarian = message.text.split(', ')
        # Validate and format the inputs
        is_halal = is_halal.lower() == 'true'
        is_vegetarian = is_vegetarian.lower() == 'true'
        
        
        add_place_api(name, description, category_id, is_halal, is_vegetarian, location_id)

        bot.reply_to(message, "Place added successfully!")
    except Exception as e:
        bot.reply_to(message, "Error in input format. Please try again.")


@bot.message_handler(commands=['delete_place'])
def delete_place(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, "You are not authorized to access this function.")
        return

    bot.reply_to(message, "Please send the ID of the place you want to delete.")
    # Use a message handler or a conversation handler to capture and process the user's response

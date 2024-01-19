from telebot import types
from config import ADMIN_USER_IDS, TOKEN
import telebot
from utils import fetch_all_places, format_places, fetch_all_categories, fetch_all_locations, add_place_api, delete_place_api

# Initialize the bot instance
from bot_instance import bot

unauthorise_message = "You are not authorized to access admin functions."

def is_user_admin(user_id):
    return user_id in ADMIN_USER_IDS


def admin_menu(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, unauthorise_message)
        return

    menu_message = "Admin Menu:\n" \
                   "/view_places - View all places\n" \
                   "/add_place - Add a new place\n" \
                   "/delete_place - Delete a place\n"
    bot.send_message(message.chat.id, menu_message)

def view_places(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, unauthorise_message)
        return

    places = fetch_all_places()  
    formatted_response = format_places(places)  
    bot.send_message(message.chat.id, formatted_response)

def add_place(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, unauthorise_message)
        return

    # Start the process by asking for a category
    bot.send_message(message.chat.id, "Please select a category:", reply_markup=get_categories_markup())

def get_categories_markup():
    categories = fetch_all_categories()  
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        markup.add(types.InlineKeyboardButton(category['category_name'], callback_data=f"cat_{category['category_name']}"))
    return markup


def category_callback(call):
    category = call.data.split('_')[1]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Please select a location:", reply_markup=get_locations_markup(category))


def get_locations_markup(category):
    locations = fetch_all_locations()  
    markup = types.InlineKeyboardMarkup()
    for location in locations:
        markup.add(types.InlineKeyboardButton(location['location_name'], callback_data=f"loc_{location['location_name']}_{category}"))
    return markup

def location_callback(call):
    location, category = call.data.split('_')[1:]
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "Please send the remaining place details in this format:\n"
                                                 "Name, Description, IsHalal (True/False), IsVegetarian (True/False)")
    bot.register_next_step_handler(msg, process_place_details, category, location)

def process_place_details(message, category, location):
    try:
        name, description, is_halal, is_vegetarian = message.text.split(', ')
        # Validate and format the inputs
        is_halal = is_halal.lower() == 'true'
        is_vegetarian = is_vegetarian.lower() == 'true'
        
        
        add_place_api(name, description, category, is_halal, is_vegetarian, location)

        bot.reply_to(message, "Place added successfully!")
    except Exception as e:
        bot.reply_to(message, "Error in input format. Please try again.")


def delete_place(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, unauthorise_message)
        return

    msg = bot.send_message(message.chat.id, "Please send the ID of the place you want to delete.")
    # Use a message handler or a conversation handler to capture and process the user's response
    bot.register_next_step_handler(msg, process_delete_place)

def process_delete_place (message):
    try: 
        id = message.text
        delete_place_api(id)

        bot.reply_to(message, "Place deleted successfully")
    except Exception as e:
        bot.reply_to(message, "You have entered an invalid ID. Please try again.")
        return


def view_category(message):
    return 
def add_category(message):
    return 
def delete_category(message):
    return 
def view_location(message):
    return 
def add_location(message):
    return 
def delete_location(message):
    return 


# Handle txt file upload
def handle_document(message): 
    if message.document.mime_type == 'text/plain':
        process_place_file(message)
    else:
        bot.reply_to(message, "Please upload a text file.")

def process_place_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Assuming the file contains one place per line, formatted as:
    # name, description, category, is_halal, is_vegetarian, location
    for line in downloaded_file.decode('utf-8').split('\n'):
        if line.strip():
            try:
                name, description, category, is_halal, is_vegetarian, location = line.split(', ')
                # Convert and validate data if necessary
                is_halal = is_halal.lower() == 'true'
                is_vegetarian = is_vegetarian.lower() == 'true'
                
                # Call your API to add the place
                # add_place_api(name, description, category, is_halal, is_vegetarian, location)
            except ValueError:
                bot.reply_to(message, f"Invalid format in line: {line}")
                return
    bot.reply_to(message, "Places added successfully.")

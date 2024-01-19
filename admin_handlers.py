import csv
import io
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
                   "/delete_place - Delete a place\n" \
                   "/export_places - Export all places to a text file\n" 
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
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, unauthorise_message)
        return
    if message.document.mime_type == 'text/csv':
        process_place_file(message)
    else:
        bot.reply_to(message, "Please upload a CSV file.")

def process_place_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        # Convert the downloaded file to a string and read it as a CSV
        csv_data = downloaded_file.decode('utf-8').splitlines()
        reader = csv.DictReader(csv_data)

        required_headers = ['id', 'name', 'description', 'category', 'is_halal', 'is_vegetarian', 'location']
        if not all(header in reader.fieldnames for header in required_headers):
            bot.reply_to(message, "CSV file missing required headers. Please check the format and try again.")
            return

        for row in reader:
            # Perform data validation and processing
            is_halal = row['is_halal'].lower().strip() == 'true'
            is_vegetarian = row['is_vegetarian'].lower().strip() == 'true'

            # Call your API to add the place
            add_place_api(row['id'].strip(), row['name'].strip(), row['description'].strip(),
                        row['category'].strip(), is_halal, is_vegetarian, row['location'].strip())

        bot.reply_to(message, "Places updated successfully.")
    except ValueError as e:
        bot.reply_to(message, f"Invalid format in CSV: {e}")
        return
    except Exception as e:
        bot.reply_to(message, f"An error occurred while processing the file: {e}")
        return



def export_places_handler(message):
    if not is_user_admin(message.from_user.id):
        bot.reply_to(message, unauthorise_message)
        return

    try:
        data = fetch_all_places()
        places = data.get('places')
        csv_buffer = format_places_for_export(places)
        
        csv_buffer.seek(0)  # Go to the start of the in-memory file
        bot.send_document(message.chat.id, ('places_export.csv', csv_buffer))
    except Exception as e:
        bot.reply_to(message, "An error occurred while exporting the places. Please try again later.")
        print("Error in export_places_handler:", e)


def format_places_for_export(places):
    csv_buffer = io.StringIO()  # Create an in-memory text stream

    fieldnames = ['id', 'name', 'description', 'category', 'is_halal', 'is_vegetarian', 'location']
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)

    writer.writeheader()
    for place in places:
        # Select only the desired keys for CSV
        csv_row = {key: place[key] for key in fieldnames}
        writer.writerow(csv_row)

    return csv_buffer
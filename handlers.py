from utils import generate_food_place, request_admin_api, generate_halal_food_place, generate_vegetarian_food_place
from bot_instance import bot

def start(message):
    welcome_message = (
       "Hello! Welcome to Time-To-Makan.\n\n"
        "I'm here to assist you in discovering great places to eat. Here's what I can do:\n"
        "- Suggest random places for your next meal with /generate.\n"
        "- Suggest Halal places with /generate_halal.\n"
        "- Suggest Vegetarian places with /generate_vegetarian.\n"
        "- Provide helpful information with /help.\n"
        "For Admins:\n"
        "- Access admin functions with /admin_menu.\n\n"
        "Start by typing a command or use /help to see all options!"
    )
    bot.send_message(message.chat.id, welcome_message)

def help(message):
    help_message = (
        "Time-To-Makan Bot Commands:\n\n"
        "/start - Learn about the bot and get started.\n"
        "/help - View this help message anytime.\n"
        "/generate - Get a random food place suggestion.\n"
        "/generate_halal - Get a Halal food place suggestion.\n"
        "/generate_vegetarian - Get a Vegetarian food place suggestion.\n"
        "/request_admin_access - Request admin privileges.\n"
        "Admins only:\n"
        "/admin_menu - Access admin-specific functions.\n\n"
        "Just type a command to begin. Need assistance? Use /help!"
    )
    bot.send_message(message.chat.id, help_message)


def generatePlace(message):
    place_response = generate_food_place()  # This should return the JSON response from your API
    if place_response:
        # Extracting the required fields from the response
        place = place_response.get('place', {})
        location = place.get('location', 'No location info')
        name = place.get('name', 'Unknown')
        is_halal = "Halal" if place.get('is_halal') else "Not Halal"
        is_vegetarian = "Vegetarian" if place.get('is_vegetarian') else "Non-Vegetarian"

        # Formatting the response message
        response_message = f"{location} - {name}, {is_halal}, {is_vegetarian}"
        bot.send_message(message.chat.id , response_message)
    else:
        # Handle cases where the response is empty or not as expected
        bot.reply_to(message, "Sorry, I couldn't find a food place suggestion at the moment.")

def generateHalalPlace(message):
    place_response = generate_halal_food_place()  
    if place_response:
        # Extracting the required fields from the response
        place = place_response.get('place', {})
        location = place.get('location', 'No location info')
        name = place.get('name', 'Unknown')
        is_halal = "Halal" if place.get('is_halal') else "Not Halal"
        is_vegetarian = "Vegetarian" if place.get('is_vegetarian') else "Non-Vegetarian"

        # Formatting the response message
        response_message = f"{location} - {name}, {is_halal}, {is_vegetarian}"
        bot.send_message(message.chat.id , response_message)
    else:
        # Handle cases where the response is empty or not as expected
        bot.reply_to(message, "Sorry, I couldn't find a food place suggestion at the moment.")

def generateVegetarianPlace(message):
    place_response = generate_vegetarian_food_place()  
    if place_response:
        # Extracting the required fields from the response
        place = place_response.get('place', {})
        location = place.get('location', 'No location info')
        name = place.get('name', 'Unknown')
        is_halal = "Halal" if place.get('is_halal') else "Not Halal"
        is_vegetarian = "Vegetarian" if place.get('is_vegetarian') else "Non-Vegetarian"

        # Formatting the response message
        response_message = f"{location} - {name}, {is_halal}, {is_vegetarian}"
        bot.send_message(message.chat.id , response_message)
    else:
        # Handle cases where the response is empty or not as expected
        bot.reply_to(message, "Sorry, I couldn't find a food place suggestion at the moment.")


def handle_unrecognized_command(message):
    response = (
        """
            I'm not sure I understand that command.\n
            Here are some things I can do for you:
            - /start: Discover what Time-To-Makan can offer.
            - /help: Get a list of available commands.
            - /generate: Receive a random suggestion for your next meal.\n
            Admins can use /admin_menu to access admin features.
            Need more assistance? Just type /help!
        """
    )
    bot.reply_to(message, response)


def request_admin(message): 
    try: 
        id = message.chat.id
        username  = message.chat.username

        response = request_admin_api(id, username)
        print(response)
        if response.get('error'):
            bot.send_message(message.from_user.id, f"{response.get('error').get('message')}")
        else:
            bot.send_message(message.from_user.id, "Request sent successfully!")
    except Exception as e: 
        bot.send_message(message.from_user.id, "An unexpected error occurred. Please try again.")
        return
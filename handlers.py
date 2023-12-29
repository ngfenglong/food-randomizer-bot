from utils import generate_food_place
from bot_instance import bot

def start(message):
    welcome_message = (
        "Hello!  Welcome to the Novena Lunch Generator.\n\n"
        "I'm here to help you decide on a place to eat for your next meal."
        "Simply use the commands below to interact with me. Let's make lunch decisions easier!"
    )
    bot.send_message(message.chat.id, welcome_message)

def help(message):
    help_message = (
        "Here are the commands you can use:\n\n"
        "/start - Welcome message and bot instructions.\n"
        "/help - Get detailed information about how to use this bot.\n"
        "/generate - Receive a random food place suggestion based on your preferences.\n\n"
        "Just type a command to get started. If you need any assistance, feel free to use the /help command anytime!"
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

def handle_unrecognized_command(message):
    response = (
        """
            Oops! I didn't recognize that command.
        
            Here's what I can help you with:
            /start - Get started and learn more about this bot.
            /help - Display the help message with command details.
            /generate - Generate a random food place suggestion.

            If you need help or have questions, just type /help. 
        """
    )
    bot.reply_to(message, response)

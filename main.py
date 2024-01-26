from handlers import start, help, generatePlace, handle_unrecognized_command, request_admin, generateHalalPlace, generateVegetarianPlace
from admin_handlers import (
    admin_menu, view_places, add_place, delete_place, 
    category_callback, location_callback, handle_document,
    view_category, add_category, delete_category, 
    view_location, add_location, delete_location, 
    export_places_handler
)

# Initialize the bot instance
from bot_instance import bot


# Public Handlers 
bot.register_message_handler(start, commands=['start', 'hello'])
bot.register_message_handler(help, commands=['help'])
bot.register_message_handler(generatePlace, commands=['generate'])
bot.register_message_handler(generateHalalPlace, commands=['generate_halal'])
bot.register_message_handler(generateVegetarianPlace, commands=['generate_vegetarian'])
bot.register_message_handler(request_admin, commands=['request_admin_access'])

# Admin Handlers 
bot.register_message_handler(admin_menu, commands=['admin_menu'])
bot.register_message_handler(view_places, commands=['view_places'])
bot.register_message_handler(delete_place, commands=['delete_place'])
bot.register_message_handler(add_place, commands=['add_place'])
bot.register_message_handler(handle_document, content_types=['document'])
bot.register_message_handler(export_places_handler, commands=['export_places'])

# Category and Location Handlers
bot.register_message_handler(view_category, commands=['view_category'])
bot.register_message_handler(add_category, commands=['add_category'])
bot.register_message_handler(delete_category, commands=['delete_category'])
bot.register_message_handler(view_location, commands=['view_location'])
bot.register_message_handler(add_location, commands=['add_location'])
bot.register_message_handler(delete_location, commands=['delete_location'])


# Register Callback Handlers
bot.register_callback_query_handler(category_callback, func=lambda call: call.data.startswith('cat_'))
bot.register_callback_query_handler(location_callback, func=lambda call: call.data.startswith('loc_'))

bot.register_message_handler(handle_unrecognized_command, func=lambda m: True)

bot.infinity_polling()

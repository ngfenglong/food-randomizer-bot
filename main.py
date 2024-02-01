from bot import handlers, admin_handlers, bot

# Public Handlers 
bot.register_message_handler(handlers.start, commands=['start', 'hello'])
bot.register_message_handler(handlers.help, commands=['help'])
bot.register_message_handler(handlers.generatePlace, commands=['generate'])
bot.register_message_handler(handlers.generateHalalPlace, commands=['generate_halal'])
bot.register_message_handler(handlers.generateVegetarianPlace, commands=['generate_vegetarian'])
bot.register_message_handler(handlers.request_admin, commands=['request_admin_access'])

# Admin Handlers 
bot.register_message_handler(admin_handlers.admin_menu, commands=['admin_menu'])
bot.register_message_handler(admin_handlers.view_places, commands=['view_places'])
bot.register_message_handler(admin_handlers.delete_place, commands=['delete_place'])
bot.register_message_handler(admin_handlers.add_place, commands=['add_place'])
bot.register_message_handler(admin_handlers.handle_document, content_types=['document'])
bot.register_message_handler(admin_handlers.export_places_handler, commands=['export_places'])

# Category and Location Handlers
bot.register_message_handler(admin_handlers.view_category, commands=['view_category'])
bot.register_message_handler(admin_handlers.add_category, commands=['add_category'])
bot.register_message_handler(admin_handlers.delete_category, commands=['delete_category'])
bot.register_message_handler(admin_handlers.view_location, commands=['view_location'])
bot.register_message_handler(admin_handlers.add_location, commands=['add_location'])
bot.register_message_handler(admin_handlers.delete_location, commands=['delete_location'])


# Register Callback Handlers
bot.register_callback_query_handler(admin_handlers.category_callback, func=lambda call: call.data.startswith('cat_'))
bot.register_callback_query_handler(admin_handlers.location_callback, func=lambda call: call.data.startswith('loc_'))

bot.register_message_handler(handlers.handle_unrecognized_command, func=lambda m: True)

bot.infinity_polling()

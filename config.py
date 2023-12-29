import os
from dotenv import find_dotenv, load_dotenv

# Check if the ENV variable is set to 'production'
# Load environment variables from .env file if not in production
if os.getenv('ENV') != 'production':
    from dotenv import load_dotenv
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)


TOKEN = os.getenv("TELEGRAM_API_KEY")
BASEURL = os.getenv("API_URL")

# Fetch and process ADMIN_USER_IDS from environment variables
admin_ids = os.getenv("ADMIN_USER_IDS", "")
ADMIN_USER_IDS = [int(user_id.strip()) for user_id in admin_ids.split(',') if user_id.strip().isdigit()]

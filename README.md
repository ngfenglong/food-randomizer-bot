# Time To Makan (TTM) Telegram Bot 🤖

This repository houses the Telegram Bot for the Time To Makan (TTM) project. The bot is designed to enhance user interaction with the TTM ecosystem, providing a seamless interface for users to access and manipulate data related to food places, categories, and locations. The bot includes features for both regular users and administrators, making it a versatile tool in the TTM suite.

> 🚨 This is an ongoing project and subject to significant changes. More features and documentation will be added as the project evolves.

## Table of Contents
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Implementations](#future-implementations)
- [Contribution](#contribution)
- [Contact](#contact)

## Technology Stack 💻
- **Language:** Python
- **Messaging Platform:** Telegram Bot API
- **Containerization:** Docker

## Getting Started 🚀
To run the TTM Telegram Bot:
1. Clone the repository.
2. Create a `.env` file in the project root with the following template:
   ```
   TELEGRAM_API_KEY = [Your Telegram Bot API Key]
   API_URL = [Your Backend API Endpoint]
   ADMIN_USER_IDS=[Your Admin Telegram User IDs]
   ```
   Replace the placeholders with your actual Telegram Bot API Key, backend API endpoint, and admin Telegram user IDs.
3. Build the Docker image using the provided Dockerfile.

## Docker Support 🐳
This project includes a Dockerfile for containerization. Utilize it to run the application within a Docker container for a consistent development and deployment environment.

## Usage 🛠️
The TTM Telegram Bot is primarily designed to interact with users on the Telegram platform, offering functionalities such as:
- Generating random food place suggestions.
- Admin functionalities to manage food places, categories, and locations.

## Project Structure 📂

The TTM Telegram Bot project consists of several key files:
```
- `admin_handlers.py`: Contains handlers for admin-specific commands within the Telegram bot.
- `bot_instance.py`: Responsible for the initialization and configuration of the Telegram bot instance.
- `config.py`: Manages the configuration and environment variables for the bot.
- `Dockerfile`: Defines the Docker configuration for building a containerized version of the application.
- `handlers.py`: Includes handlers for general bot commands and user interactions.
- `main.py`: The main entry point of the bot application, where the bot is run and handlers are registered.
- `requirements.txt`: Lists all the Python dependencies required for the project.
- `utils.py`: Provides utility functions for interacting with the TTM backend API.
```


## Future Implementations 🔮
- Bulk insertion of places via text files.
- Enhanced admin functionalities for managing categories and locations.

## Contribution 🤝
Contributions, ideas, and feedback are welcome! Feel free to fork the repository and submit pull requests.

## Contact 📧
For any inquiries or clarifications related to this project, please contact [zell_dev@hotmail.com](mailto:zell_dev@hotmail.com).

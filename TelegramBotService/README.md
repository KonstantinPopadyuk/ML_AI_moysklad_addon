# Telegram Bot Service

## Overview
This service implements a Telegram bot using the `aiogram` framework, designed to handle user interactions, process commands, and integrate with Kafka for AI agent communication. The bot supports custom filters, keyboard interactions, and user authorization.

## Key Features
- **User Authorization**: Restricts access to specific users using `AllowedUserFilter`
- **Command Handling**: Processes `/start` command and custom button interactions
- **Kafka Integration**: Communicates with AI agents through Kafka topics
- **Custom Filters**: Implements filters for button text and user authorization
- **Reply Keyboards**: Provides interactive keyboard buttons for user input

## Project Structure
```
TelegramBotService/
├── filters/                  # Custom message filters
│   ├── __init__.py
│   ├── allowed_users.py      # User authorization filter
│   └── not_button_text.py    # Filter for non-button text
├── keyboards/                # Reply keyboard implementations
│   ├── __init__.py
│   └── mainkb.py             # Main keyboard layout
├── routers/                  # Message handlers
│   ├── __init__.py
│   ├── aianswers.py          # AI agent communication handler
│   ├── not_allowed.py        # Unauthorized user handler
│   └── start_commands.py     # Command handlers
├── settings.py               # Environment configuration
├── telegram_service.py       # Main bot service class
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
└── Dockerfile                # Container configuration
```

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   KAFKA_BROKER=localhost:9092
   ```

## Running the Service
### Local Development

```bash
python main.py
```

### Docker
```bash
docker build -t telegram-bot .
docker run -it --env-file .env telegram-bot
```

## Configuration
Environment variables:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `KAFKA_BROKER`: Kafka broker address (default: localhost:9092)

## Key Components
### Filters
- `AllowedUserFilter`: Restricts access to authorized users
- `NotButtonTextFilter`: Filters out predefined button texts

### Routers
- `start_commands.py`: Handles `/start` command and button interactions
- `aianswers.py`: Manages communication with AI agents via Kafka
- `not_allowed.py`: Handles unauthorized user messages

### Keyboards
- `mainkb.py`: Implements the main reply keyboard with buttons

## Kafka Integration
The service communicates with AI agents through Kafka topics:
- `requests_to_AI_agents`: Sends user messages to AI agents
- `AI_agents_answers`: Receives responses from AI agents

## License
MIT License. See [LICENSE](LICENSE) for more information.

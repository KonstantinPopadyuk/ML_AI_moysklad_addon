from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from routers import start_router, aianswers_router, notallowed_users_router

class TelegramService:
    def __init__(self, token: str):
        """Initialize the Telegram service with the bot token."""
        self.bot = Bot(token=token, 
                       default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.storage = MemoryStorage()
        self.dispatcher = Dispatcher(storage=self.storage)

    def run(self):
        """Start the Telegram bot."""
        self.dispatcher.include_router(start_router)
        self.dispatcher.include_router(aianswers_router)
        self.dispatcher.include_router(notallowed_users_router)
        self.dispatcher.run_polling(self.bot)
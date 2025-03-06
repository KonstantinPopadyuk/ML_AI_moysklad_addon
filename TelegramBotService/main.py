from settings import settings
import logging
import sys
from telegram_service import TelegramService

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info('Starting bot')
    try:
        TOKEN = settings.TELEGRAM_BOT_TOKEN
        telegram_service = TelegramService(TOKEN)
        logger.info(f'Successful')
        telegram_service.run() 
    except Exception as e:
        logger.error(f'Can not start bot, not valid TOKEN  /{e}/')
    
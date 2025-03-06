from aiogram import Router
from aiogram.types import Message
import logging

notallowed_users_router = Router()
logger = logging.getLogger(__name__)

@notallowed_users_router.message()
async def handle_unauthorized(message: Message):
    await message.answer("Access denied. You are not authorized to use this bot.")
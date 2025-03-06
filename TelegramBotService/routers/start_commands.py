from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from filters import allowed_users_filter
import logging
from keyboards import get_main_kb

start_router = Router()
logger = logging.getLogger(__name__)

@start_router.message(CommandStart(), allowed_users_filter)
async def cmd_start(message: Message):
    print('hello world')
    await message.answer('Привет! Жду вопроса с которым могу помочь',
                         reply_markup=get_main_kb())
    
@start_router.message(F.text == "Продажи за месяц", allowed_users_filter)
async def cmd_start(message: Message):
    response = 'some great answer'
    await message.answer(response,
                         reply_markup=ReplyKeyboardRemove())
    
@start_router.message(F.text == "Топ-10 товары", allowed_users_filter)
async def cmd_start(message: Message):
    response = 'some great answer'
    await message.answer(response,
                         reply_markup=ReplyKeyboardRemove())
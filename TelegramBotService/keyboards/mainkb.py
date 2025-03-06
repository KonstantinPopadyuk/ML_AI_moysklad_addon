from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Продажи за месяц")
    kb.button(text="Топ-10 товары")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
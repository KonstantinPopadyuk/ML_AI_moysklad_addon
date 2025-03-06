from aiogram import F
from aiogram.filters import Filter
from aiogram.types import Message

class NotButtonTextFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        # Список текстов кнопок, которые нужно исключить
        button_texts = ["Продажи за месяц", "Топ-10 товары"]
        return message.text not in button_texts 
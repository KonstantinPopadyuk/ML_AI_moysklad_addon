from aiogram import Router, F
from aiogram.types import Message
from filters import allowed_users_filter, NotButtonTextFilter
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import tabulate
from typing import Dict, List
from aiogram.enums import ParseMode
import re

async def start_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=['kafka:9092'])
    await producer.start()
    return producer

async def start_consumer() -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        'AI_agents_answers',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='latest'
    )
    await consumer.start()
    return consumer

aianswers_router = Router()
logger = logging.getLogger(__name__)

@aianswers_router.message(F.text, NotButtonTextFilter(), allowed_users_filter)
async def cmd_start_4(message: Message):
    producer = await start_producer()
    consumer = await start_consumer()

    response = {'message': message.text, 'user_id': message.from_user.id, 'message_id': message.message_id}
    response = json.dumps(response).encode(encoding="utf-8")
    await producer.send('requests_to_AI_agents', response)
    try:
        async for ans in consumer:
            decoded_message = json.loads(ans.value)
            if (message.from_user.id == decoded_message['user_id'] and
                message.message_id == decoded_message['message_id']):
            # construction 'if -> break' works (received one message -> read and reply only to it) but not sure that will be good
            # if message.from_user.id == decoded_message['user_id']:
                decoded_message = json.loads(ans.value)
                # ans = f"Ваше сообщение '{message.text}' получило ответ'{decoded_message['message']}'\n и табличку {decoded_message['table']} \n Предлагаю просто представить что мы на него ответили с помощью AI"
                if decoded_message['table']:
                    #TASK If table to long - convert to .csv
                    await message.answer(f'Первые 20 строк отчета: <pre>{format_sales_table(data=decoded_message['table']['data'])}</pre>', parse_mode=ParseMode.HTML)
                # logger.info(f'Received {message.text} from user_id = {message.from_user.id}')
                escaped_summary = escape_markdown(decoded_message['message'])
                await message.answer(escaped_summary, parse_mode=ParseMode.MARKDOWN_V2)
                # await message.answer(decoded_message['message'])
            # break
    finally:
        await consumer.stop()
        await producer.stop()


def format_sales_table(data: List[Dict]) -> str:
    # Переименование заголовков
    # headers = {
    #     'agent_name': 'Клиент',
    #     'orders_count': 'Заказы',
    #     'item_mean_price': 'Ср. цена товара',
    #     'order_mean_sum': 'Ср. сумма заказа',
    #     'orders_total_sum': 'Общая сумма'
    # }

    # # Форматирование чисел
    # formatted_data = []
    # for row in data:
    #     formatted_row = {
    #         'agent_name': row['agent_name'],
    #         'orders_count': row['orders_count'],
    #         'item_mean_price': f"{row['item_mean_price']:,.2f} ₽".replace(",", " "),
    #         'order_mean_sum': f"{row['order_mean_sum']:,.2f} ₽".replace(",", " "),
    #         'orders_total_sum': f"{row['orders_total_sum']:,.2f} ₽".replace(",", " ")
    #     }
    #     formatted_data.append(formatted_row)
    formatted_data = data[:20]
    # Генерация таблицы в формате Markdown
    table_content = tabulate.tabulate(
        [row.values() for row in formatted_data],
        headers=formatted_data[0].keys(),
        tablefmt="pipe",
        stralign="right",
        numalign="right"
    )
    return table_content


def escape_markdown(text):
    # Экранируем специальные символы для Markdown_v2
    escape_chars = r'_[]()~`>#+-=|{}.!'
    return re.sub('([' + re.escape(escape_chars) + '])', r'\\\1', text)
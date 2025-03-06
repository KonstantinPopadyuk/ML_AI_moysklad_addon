from tabulate import tabulate
from typing import Dict, Any, List, Optional
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

async def start_consumer() -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        'requests_to_AI_agents',
        bootstrap_servers=['kafka:9092'],
        # group_id=f"ai_consumer_all_chats",
        auto_offset_reset='latest'
    )
    await consumer.start()
    return consumer

async def start_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=['kafka:9092'])
    await producer.start()
    return producer

def format_sales_table(self, data: List[Dict]) -> str:
    # Переименование заголовков
    headers = {
        'agent_name': 'Клиент',
        'orders_count': 'Заказы',
        'item_mean_price': 'Ср. цена товара',
        'order_mean_sum': 'Ср. сумма заказа',
        'orders_total_sum': 'Общая сумма'
    }

    # Форматирование чисел
    formatted_data = []
    for row in data:
        formatted_row = {
            'agent_name': row['agent_name'],
            'orders_count': row['orders_count'],
            'item_mean_price': f"{row['item_mean_price']:,.2f} ₽".replace(",", " "),
            'order_mean_sum': f"{row['order_mean_sum']:,.2f} ₽".replace(",", " "),
            'orders_total_sum': f"{row['orders_total_sum']:,.2f} ₽".replace(",", " ")
        }
        formatted_data.append(formatted_row)

    # Генерация таблицы в формате Markdown
    table_content = tabulate(
        [row.values() for row in formatted_data],
        headers=headers.values(),
        tablefmt="pipe",
        stralign="right",
        numalign="right"
    )
    return table_content
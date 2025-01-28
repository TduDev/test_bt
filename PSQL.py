from aiogram.types import BotCommand
import asyncpg
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

menu_of_bot = {
    BotCommand(command='pos', description='Позиции технического товара, которые есть в наличии'),
    BotCommand(command='about', description='О нас'),
    BotCommand(command='payment', description='Варианты оплаты'),
    BotCommand(command='delivery', description='Все о доставке')
}

words_to_cya = ['1']
hello_words = ['2']
bad_words = ['3']


async def take_base_info(positions):
    conn = await asyncpg.connect(
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        port=os.getenv('port')
    )
    try:
        query = f"SELECT * FROM positions_que WHERE iphone LIKE $1"
        products = await conn.fetch(query, f"%{positions}%")
    finally:
        await conn.close()

    return products

from aiogram import Router
from aiogram import types, F
from aiogram.filters import CommandStart, Command, or_f

from keyboard.inline_kb import logger
from PSQL import hello_words, words_to_cya

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


new_private_router = Router()


@new_private_router.message(CommandStart())
async def command_start_message(message: types.Message) -> None:
    """
    Этот обработчик реагирует на команду /start и отправляет пользователю приветственное сообщение.
    Логирует информацию о старте команды и отправляет сообщение с приветствием.
    """
    logger.info("/start logger")
    user_id = message.from_user.first_name
    await message.answer(f'{user_id}, привет! Я виртуальный помощник.\n Вся информация в меню слева.')


@new_private_router.message(F.text.lower() == 'about')
@new_private_router.message(Command('about'))
async def abount_us(message: types.Message) -> None:
    """
    Этот обработчик реагирует на команду /about или сообщение 'about' и отправляет информацию о компании.
    Логирует информацию о запросе и отправляет сообщение с информацией.
    """
    logger.info('/about us logger')
    await message.answer(f"{os.getenv('dsds')}")


@new_private_router.message(or_f(F.text.lower().contains('оплат'), F.text.lower().contains('цен')))
@new_private_router.message(Command('payment'))
async def payment_answer(message: types.Message) -> None:
    """
    Этот обработчик реагирует на команду /payment и сообщения, содержащие слова 'оплат' или 'цен'.
    Логирует запрос на оплату и отправляет соответствующую информацию.
    """
    logger.info('/payment logger')
    await message.answer(f"{os.getenv('payment')}")


@new_private_router.message(Command('delivery'))
@new_private_router.message(or_f(F.text.lower().contains('доставк')))
async def deliviry_answer(message: types.Message) -> None:
    """
    Этот обработчик реагирует на команду /delivery и сообщения, содержащие слово 'доставк'.
    Логирует запрос на доставку и отправляет соответствующую информацию.
    """
    logger.info('/delivery logger')
    await message.answer(f"{os.getenv('delivery')}")


@new_private_router.message(~F.text.startswith('/'))
async def answer_message_of_users(message: types.Message) -> None:
    """
    Этот обработчик отвечает на любые сообщения, не начинающиеся с '/'.
    Если сообщение содержит приветствие, отправляется приветствие, если прощание — прощание.
    В остальных случаях отправляется стандартный ответ.
    """
    text = message.text.lower()
    if text in hello_words:  # Проверка, если текст в списке приветствий
        await message.answer(f'Здравствуйте, {message.from_user.first_name}! Для старта, нажмите /start')
    elif text in words_to_cya:  # Проверка, если текст в списке прощаний
        await message.answer(f'Cya, {message.from_user.first_name}!')
    else:  # Ответ по умолчанию для остальных сообщений
        await message.answer('Если остались вопросы, нажмите /start')
        logger.info("After all")

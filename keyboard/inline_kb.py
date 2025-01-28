from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from PSQL import take_base_info
from filters.castom_filters import MyCustomFilter

inline_router = Router()
inline_router.message.filter(MyCustomFilter(['private']))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def create_keyboard(items, back=True):
    """
    Функция для создания клавиатуры с кнопками для inline-кнопок.
    Аргументы:
    - items: Список словарей, содержащих текст и callback_data для каждой кнопки.
    - back: Флаг, указывающий, нужно ли добавлять кнопку 'Назад'.
    Возвращает: Клавиатуру в формате InlineKeyboardMarkup.
    """
    keyboard = []
    for item in items:
        # Добавляем кнопки из списка items
        keyboard.append([InlineKeyboardButton(text=item['text'], callback_data=item['callback_data'])])
    if back:
        # Добавляем кнопку 'Назад', если флаг back установлен в True
        keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back')])
    logger.info(f"{keyboard}")  # Логируем созданную клавиатуру
    return InlineKeyboardMarkup(inline_keyboard=keyboard)  # Возвращаем клавиатуру

@inline_router.message(Command('pos'))
async def buttons_click(message: types.Message):
    """
    Обработчик команды /pos.
    При получении команды /pos пользователю предлагается выбрать товар.
    """
    logger.info("Команда /pos получена от пользователя %s", message.from_user.username)
    await message.reply("Выберите товар:", reply_markup=create_main_keyboard())  # Отправляем основную клавиатуру

def create_main_keyboard():
    """
    Функция для создания основной клавиатуры с кнопками выбора товара.
    Возвращает: InlineKeyboardMarkup с кнопками для выбора товаров.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Iphone 📱', callback_data='iphone')],
        [InlineKeyboardButton(text='Ipad ⌨', callback_data='ipad')],
        [InlineKeyboardButton(text='MacBook 🖥', callback_data='macbook')]
    ])

@inline_router.callback_query()
async def answer_of_saller(callback: types.CallbackQuery) -> None:
    """
    Обработчик callback-запросов.
    Проверяет callback_data и в зависимости от выбора пользователя
    вызывает соответствующую обработку.
    """
    if callback.data.startswith('~'):
        # Если callback_data начинается с '~', рекурсивно вызываем обработку (необычное поведение)
        # (по факту костыль, не работает почему-то через F)
        await answer_of_saller(callback)
    else:
        await result_button_click(callback)  # Иначе передаем в другую функцию для обработки

@inline_router.callback_query()
async def result_button_click(callback: types.CallbackQuery) -> None:
    """
    Обработчик выбора модели товара.
    В зависимости от callback_data (iphone, ipad, macbook),
    подбираются соответствующие модели и обновляется клавиатура.
    """
    if callback.data == 'iphone':
        # Обработка выбора Iphone
        logger.info(f"iphone {callback.data}")
        items = [
            {'text': 'Iphone 12', 'callback_data': '~iphone_12'},
            {'text': 'Iphone 13', 'callback_data': '~iphone_13'},
            {'text': 'Iphone 14', 'callback_data': '~iphone_14'},
            {'text': 'Iphone 15', 'callback_data': '~iphone_15'}
        ]
        await callback.message.edit_text('Выберите модель iPhone:', reply_markup=create_keyboard(items))

    elif callback.data == 'ipad':
        # Обработка выбора iPad
        logger.info(f"ipad {callback.data}")
        items = [
            {'text': 'iPad Pro 12.9 (2021)', 'callback_data': '~ipad_pro'},
            {'text': 'iPad 2020', 'callback_data': '~ipad_2020'},
            {'text': 'iPad mini 2021', 'callback_data': '~ipad_mini'},
            {'text': 'Apple iPad 10.2 (2021)', 'callback_data': '~ipad_10_2'}
        ]
        await callback.message.edit_text('Выберите модель iPad:', reply_markup=create_keyboard(items))

    elif callback.data == 'macbook':
        # Обработка выбора MacBook
        logger.info(f"macbook {callback.data}")
        items = [
            {'text': 'MacBook Air', 'callback_data': '~macbook_air'},
            {'text': 'MacBook Pro 13"', 'callback_data': '~macbook_pro_13'},
            {'text': 'MacBook Pro 16"', 'callback_data': '~macbook_pro_16'}
        ]
        await callback.message.edit_text('Выберите модель MacBook:', reply_markup=create_keyboard(items))

    elif callback.data == 'back':
        # Обработка кнопки 'Назад'
        logger.info(f"back {callback.data}")
        await callback.message.edit_text("Выберите товар:", reply_markup=create_main_keyboard())

@inline_router.callback_query()
async def answer_of_saller(callback: types.CallbackQuery) -> None:
    """
    Обработчик получения информации о товаре.
    Получает информацию о товаре по callback_data, обращаясь к базе данных.
    """
    logger.info('/take answer')
    result = await take_base_info(callback.data[1:].lower())  # Запрашиваем информацию из базы по данным callback_data
    if result:
        # Если товар найден, выводим информацию о нем
        for elem in result:
            ans = f"{elem[1]}     кол-во: {elem[2]}      цвет: {elem[3]}     память: {elem[4]}"
            await callback.message.answer(ans)
    else:
        # Если товар не найден
        await callback.message.answer("Товар отсуствует.")


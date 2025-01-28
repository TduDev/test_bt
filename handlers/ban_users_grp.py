import logging
import asyncio
from aiogram import Router, types
from datetime import timedelta, datetime

from PSQL import bad_words
from filters.castom_filters import MyCustomFilter

grp_router = Router()
logger = logging.getLogger('handlers.tracking_private')

grp_router.message.filter(MyCustomFilter(['group']))

list_of_users = {}
ban_users = {}



def check_ban_status(usr_id: int) -> bool:
    """
    Эта функция проверяет, заблокирован ли пользователь. Если пользователь заблокирован,
    возвращает True, иначе — False. Если блокировка истекла, она удаляет пользователя из списка заблокированных.
    """
    if usr_id in ban_users and ban_users[usr_id] > datetime.now():
        logger.info(f"Пользователь {usr_id} в данный момент заблокирован.")
        return True
    elif usr_id in ban_users and ban_users[usr_id] <= datetime.now():
        del ban_users[usr_id]
        logger.info(f"Блокировка пользователя {usr_id} истекла.")
    return False



def process_bad_words(message_text: str) -> list[str]:
    """
    Эта функция принимает текст сообщения, фильтрует его, удаляя все символы, кроме букв и пробелов,
    и возвращает список слов, из которых состоит очищенный текст.
    """
    filtered_words = ''.join(word for word in message_text if word.isalpha() or word == ' ')
    return filtered_words.split()



async def ban_user(usr_id: int, duration: int) -> None:
    """
    Эта функция блокирует пользователя на определенное количество секунд.
    По истечении времени блокировка снимается автоматически.
    """
    ban_users[usr_id] = datetime.now() + timedelta(seconds=duration)
    logger.info(f"Пользователь {usr_id} заблокирован на {duration} секунд.")
    await asyncio.sleep(duration)
    if usr_id in ban_users:
        del ban_users[usr_id]
    logger.info(f"Пользователь {usr_id} был разблокирован.")



@grp_router.message()
async def filter_ban_users(message: types.Message) -> None:
    """
    Эта функция обрабатывает каждое сообщение от пользователя. Она проверяет, заблокирован ли пользователь,
    и если он заблокирован, удаляет его сообщение. Также проверяет наличие запрещенных слов в сообщении
    и в случае их нахождения увеличивает счетчик нарушений пользователя. Если нарушений набирается 5,
    пользователь блокируется на 60 секунд.
    """
    usr_id = message.from_user.id

    # Проверка состояния блокировки пользователя.
    if check_ban_status(usr_id):
        await message.delete()
        logger.info(f"Сообщение от заблокированного пользователя {usr_id} было удалено.")
        return

    # Инициализация счетчика нарушений для нового пользователя.
    if usr_id not in list_of_users:
        list_of_users[usr_id] = 0
        logger.info(f"Пользователь {usr_id} добавлен в список отслеживания с нулевым счетчиком нарушений.")

    # Обработка текста сообщения и проверка на наличие плохих слов
    for word in process_bad_words(message.text):
        if word.lower() in bad_words:
            list_of_users[usr_id] += 1
            await message.delete()
            logger.info(f"Сообщение пользователя {usr_id} удалено за использование запрещенного слова: {word}")
            await message.answer(f"{message.from_user.first_name}, сообщение удалено за нарушение правил сообщества!")

            # Блокировка пользователя при достижении лимита нарушений
            if list_of_users[usr_id] == 5:
                await message.answer(f"{message.from_user.first_name}, Вы были заблокированы на 60 сек")
                logger.info(f"Пользователь {usr_id} достиг лимита нарушений и будет заблокирован.")
                list_of_users[usr_id] = 0
                await ban_user(usr_id, 60)
                return



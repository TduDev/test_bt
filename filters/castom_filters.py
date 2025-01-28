from aiogram import types
from aiogram.filters import BaseFilter


class MyCustomFilter(BaseFilter):
    """
    Кастомный фильтр для обработки сообщений на основе типа чата.

    :param chat_types: список типов чатов, для которых фильтр должен срабатывать.
    """

    def __init__(self, chat_types: list[str]) -> None:
        """
        Инициализирует фильтр, сохраняя список допустимых типов чатов.

        :param chat_types: список типов чатов, например.
        """
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        """
        Проверяет, относится ли тип чата сообщения к одному из допустимых.

        :param message: сообщение, отправленное пользователем.
        :return: True, если тип чата сообщения находится в списке допустимых, иначе False.
        """
        return message.chat.type in self.chat_types

from aiogram import Bot, types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import os
import asyncio

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from handlers.private import new_private_router
from keyboard.inline_kb import inline_router
from PSQL import menu_of_bot
from handlers.ban_users_grp import grp_router

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(inline_router)
dp.include_router(grp_router)
dp.include_router(new_private_router)


async def start_bot_using():
    await bot.set_my_commands(commands=menu_of_bot, scope=types.BotCommandScopeAllPrivateChats())
    # Удалить меню команд
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot_using())










    




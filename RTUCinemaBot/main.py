import asyncio

from aiogram import Bot, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_API

loop = asyncio.new_event_loop()
bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)

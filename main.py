import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import h1_startup, h2_get_contact

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h1_startup.router)
dp.include_router(h2_get_contact.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
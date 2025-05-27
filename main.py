import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import handlers01_startup


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(handlers01_startup.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
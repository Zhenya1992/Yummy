import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import (
    h1_startup, h2_get_contact, h3_make_order, h4_categories,
    h5_navigation, h6_product_detail
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h1_startup.router)
dp.include_router(h2_get_contact.router)
dp.include_router(h3_make_order.router)
dp.include_router(h4_categories.router)
dp.include_router(h5_navigation.router)
dp.include_router(h6_product_detail.router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
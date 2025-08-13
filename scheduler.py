import os
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram import Bot
from dotenv import load_dotenv
from database.utils import db_get_last_order_info

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("TOKEN")
MANAGER_CHAT_ID = int(os.getenv("MANAGER_CHAT_ID", "0"))


if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/reminders.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL)
}
scheduler = AsyncIOScheduler(jobstores=jobstores)


async def remind_manager(order_id: int, manager_chat_id: int):

    async with Bot(token=BOT_TOKEN) as bot:
        try:
            order_info = db_get_last_order_info(order_id)
            if not order_info:
                logger.error(f"Заказ с ID {order_id} не найден")
                return

            text = (
                f" Напоминание: заказ №{order_id}\n"
                f"Клиент: {order_info['username']}\n"
                f"Телефон: {order_info['phone']}\n"
                f"Сумма заказа: {order_info['total_price']:.2f} BYN"
            )

            await bot.send_message(manager_chat_id, text)
            logger.info(f"Напоминание  отправлено (order_id={order_id})")

        except Exception as e:
            logger.exception(f"Ошибка при отправке напоминания: {e}")


def schedule_reminder(order_id: int):

    run_date = datetime.now() + timedelta(seconds=3)
    scheduler.add_job(
        remind_manager,
        "date",
        run_date=run_date,
        args=[order_id, MANAGER_CHAT_ID],
        id=f"reminder_{order_id}",
        replace_existing=True
    )
    logger.info(f"Задача для заказа {order_id} запланирована на {run_date}")


def start_scheduler():

    if not scheduler.running:
        scheduler.start()
        logger.info("Планировщик запущен")
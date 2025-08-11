import os
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram import Bot
import logging
from dotenv import load_dotenv

from database.utils import db_get_order_info

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('TOKEN')
MANAGER_ID = int(os.getenv('MANAGER_ID','0'))


if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)


async def manage_scheduler(cart_id, manager_id):
    """Управление планировщиком"""

    bot = Bot(token=BOT_TOKEN)

    order_info = db_get_order_info(cart_id)

    if not order_info:
        logger.error(f'Заказ {cart_id} не найден')
        await bot.session.close()
        return

    text = (
        f"Заказ с номером: {cart_id} \n"
        f"Клиент: {order_info['username']}\n"
        f"Сумма: {order_info['total_price']:.2f} BYN"
    )

    await bot.send_message(manager_id, text)
    await bot.session.close()
    logger.info(f"Напоминание менеджеру отправлено")


def schedule_time(cart_id):
    """Планирование времени напоминания"""

    run_date = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(
        manage_scheduler,
        "date",
        run_date=run_date,
        args=[cart_id, MANAGER_ID],
        id=f"reminder_{cart_id}",
        replace_existing=True,
    )
    logger.info(f"Напоминание для заказа {cart_id} запланировано на {run_date}")


def start_scheduler():
    """Запуск планировщика"""

    if not scheduler.running:
        scheduler.start()
        logger.info('Планировщик запущен.')
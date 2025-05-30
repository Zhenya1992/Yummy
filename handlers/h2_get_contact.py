from aiogram import Router, F
from aiogram.types import Message

from database.utils import db_update_user, db_create_user_cart

router = Router()

@router.message(F.contact)
async def handle_update_user(message: Message):
    """Обновление юзеров"""

    chat_id = message.chat.id
    phone = message.contact.phone_number
    print(f"{chat_id=} {phone=}")

    db_update_user(chat_id, phone)

    if db_create_user_cart(chat_id):
        await message.answer(text='Регистрация прошла успешно!')
    await show_main_menu(message)


async def show_main_menu(message: Message):
    """Показ главного меню"""

    await message.answer(
        text='Сделайте свой выбор',
    ) # здесь будет кнопка маин меню
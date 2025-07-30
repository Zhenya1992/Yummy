from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from database.utils import db_register_user, db_is_registered
from handlers.h2_get_contact import show_main_menu
from keyboards.reply_kb import phone_button, first_button
from log_actions import log_register_user

router = Router()


@router.message(F.text == 'Добро пожаловать! 👋')
async def welcome_handler(message: Message):
    """Обработчик реакции на команду старт"""

    await greet_handler(message)


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """Обработчик реакции на команду старт и ссылку"""

    photo = FSInputFile("media/greet.jpg")
    if db_is_registered(message.chat.id):

        await message.answer_photo(
            photo=photo,
            caption=f"С возвращением 😊, <i>{message.from_user.full_name}</i>!",
            parse_mode='HTML',
            reply_markup=first_button(),
        )

    else:
        await message.answer_photo(
            photo=photo,
            caption=f"Добро пожаловать, <b>{message.from_user.full_name}</b>\nДля работы с ботом, предоставьте Ваш номер телефона!",
            parse_mode='HTML',
            reply_markup=phone_button()
        )


async def greet_handler(message: Message):
    """Корутина приветствия пользователя"""

    await register_user(message)


async def register_user(message: Message):
    """Корутина регистрации пользователя"""

    chat_id = message.chat.id
    full_name = message.from_user.full_name

    log_register_user(username=full_name)

    if db_register_user(full_name, chat_id):
        await message.answer(text='Приветствуем Вас 😊')
        await show_main_menu(message)
    else:
        await message.answer(
            text='Для работы с ботом, предоставьте Ваш номер телефона!',
            reply_markup=phone_button()
        )

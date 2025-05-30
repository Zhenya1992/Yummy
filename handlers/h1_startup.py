from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, FSInputFile

from database.utils import db_register_user
from keyboards.reply_kb import start_keyboard, phone_button

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """Обработчик реакции на команду старт"""

    photo = FSInputFile("media/greet.jpg")
    await message.answer_photo(
        photo=photo,
        caption=f"Добро пожаловать, {message.from_user.full_name}!",
        reply_markup=start_keyboard()
    )
    print(message.from_user.full_name, message.from_user.username)


@router.message(CommandStart(deep_link='start'))
async def command_link_start(message: Message):
    """Обработчик реакции на ссылку"""

    photo = FSInputFile("media/greet.jpg")
    await message.answer_photo(
        photo=photo,
        caption=f"Добро пожаловать, <b>{message.from_user.full_name}</b>!",
        parse_mode='HTML',
        reply_markup=start_keyboard()
    )


@router.message(Text('Начать 🎂'))
async def handle_start_button(message: Message):
    """Обработчик реагирующей на кнопку 'Начать 🎂'"""
    await handle_start(message)


async def handle_start(message: Message):
    """Корутина реакции на кнопку 'Начать 🎂'"""
    await register_user(message)


async def register_user(message: Message):
    """Корутина регистрации пользователя"""
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    print(full_name)

    if db_register_user(chat_id, full_name):
        await message.answer(text='Приветствуем Вас 😊')
        await show_main_menu(message)
    else:
        await message.answer(
            text='Для работы с ботом, предоставьте Ваш номер телефона!',
            reply_markup=phone_button()
        )
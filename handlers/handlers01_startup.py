from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from keyboards.reply_kb import start_keyboard


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
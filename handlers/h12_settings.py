from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline_kb import show_settings_menu


router = Router()


@router.message(F.text =='Настройки ⚙️')
async def handle_settings(message: Message):
    """Обработчик настроек"""

    await message.answer(text="Настройки 🖥️", reply_markup=show_settings_menu())
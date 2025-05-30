from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def start_keyboard():
    """Кнопка для старта бота"""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Начать 🎂')]],
        resize_keyboard=True
    )


def phone_button():
    """Кнопка для отправки номера телефона"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить номер телефона 📞", request_contact=True)
    return builder.as_markup(resize_keyboard=True)
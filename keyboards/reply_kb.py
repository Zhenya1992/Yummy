from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


def start_keyboard():
    """Кнопка для старта бота"""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Начать 🎂')]],
                  resize_keyboard=True
    )
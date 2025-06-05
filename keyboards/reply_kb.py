from aiogram.utils.keyboard import ReplyKeyboardBuilder


def phone_button():
    """Кнопка для отправки номера телефона"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить номер телефона 📞", request_contact=True)
    return builder.as_markup(resize_keyboard=True)


def get_main_menu():
    """Функция для получения главного меню"""

    builder = ReplyKeyboardBuilder()
    builder.button(text='Сделать заказ')
    builder.button(text='История заказов')
    builder.button(text='Корзина')
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)
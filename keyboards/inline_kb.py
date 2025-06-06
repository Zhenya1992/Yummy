from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_all_categories, db_get_finally_price


def show_category_menu(chat_id):
    """Функция показа категорий товара"""

    categories = db_get_all_categories()
    total_price = db_get_finally_price(chat_id)

    builder = InlineKeyboardBuilder()
    [builder.button(text=category.category_name, callback_data=f"category_{category.id}") for category in categories]

    builder.button(
        text=f"Сумма заказа ({total_price if total_price else '0'}руб.)",
        callback_data="Сумма заказа",
    )

    builder.adjust(1, 2)
    return builder.as_markup()
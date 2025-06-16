from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.models import Products
from database.utils import db_get_all_categories, db_get_finally_price, db_get_products_from_category



def show_category_menu(chat_id):
    """Кнопка показа категорий товара"""

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


def show_product_by_category(category_id):
    """Кнопка показа товаров по категории"""

    products = db_get_products_from_category(category_id)

    builder = InlineKeyboardBuilder()
    [builder.button(text=product.product_name, callback_data=f"product_{product.id}") for product in products]

    builder.adjust(1, 2)
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="Назад"))

    return builder.as_markup()


def cart_quantity_controller(quantity=1):
    """Кнопка контроллера количества товара"""

    builder = InlineKeyboardBuilder()
    builder.button(text="➕", callback_data="action +")
    builder.button(text=str(quantity), callback_data="quantity")
    builder.button(text="➖", callback_data="action -")
    builder.button(text= "🧺 Добавить в корзину", callback_data="Положить в корзину")

    builder.adjust(3, 1)

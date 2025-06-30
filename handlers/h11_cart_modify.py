from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_products_for_delete

router = Router()


@router.callback_query(F.data == "add")
async def choose_add_to_cart(callback: CallbackQuery):
    """Обработчик кнопки 'Увеличить количество' в корзине"""

    cart_products = db_get_products_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f"➕ {name}", callback_data=f"increase_{cart_id}")
    builder.button(text='Назад', callback_data='back_to_cart_review')
    builder.adjust(1)
    await callback.message.edit_text('Выберите товар для увеличения количества:', reply_markup=builder.as_markup())
    await callback.answer()

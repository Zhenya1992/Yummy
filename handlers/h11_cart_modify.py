from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_products_for_delete, db_increase_product_quantity, db_decrease_product_quantity, \
    db_get_cart_items
from keyboards.inline_kb import cart_action_controller
from keyboards.reply_kb import back_to_main_menu

router = Router()


@router.callback_query(F.data == "add")
async def choose_add_to_cart(callback: CallbackQuery):
    """Обработчик кнопки 'Добавления товаров' в корзине"""

    cart_products = db_get_products_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f"➕ {name}", callback_data=f"increase_{cart_id}")
    builder.button(text='Назад', callback_data='back_to_cart_review')
    builder.adjust(1)
    await callback.message.edit_text('Выберите товар для увеличения количества:', reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "remove")
async def choose_add_to_cart(callback: CallbackQuery):
    """Обработчик кнопки 'Удаления товаров' в корзине"""

    cart_products = db_get_products_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f"➖ {name}", callback_data=f"decrease_{cart_id}")
    builder.button(text='Назад', callback_data='back_to_cart_review')
    builder.adjust(1)
    await callback.message.edit_text('Выберите товар для уменьшения количества:', reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("increase_"))
async def increase_quantity(callback: CallbackQuery):
    """Обработчик кнопки 'Увеличить количество' в корзине"""

    cart_id = int(callback.data.split('_')[1])
    db_increase_product_quantity(cart_id)
    await callback.answer(text='Количество товара увеличено!')
    await choose_add_to_cart(callback)


@router.callback_query(F.data.startswith("decrease_"))
async def decrease_quantity(callback: CallbackQuery):
    """Обработчик кнопки 'Уменьшить количество' в корзине"""

    cart_id = int(callback.data.split('_')[1])
    db_decrease_product_quantity(cart_id)

    user_id = callback.from_user.id
    cart_items = db_get_cart_items(user_id)

    if not cart_items:
        await callback.message.edit_text('Ваш корзина пуста!', reply_markup=back_to_main_menu())
    else:
        text = '🧺 Содержимое корзины:\n\n'
        total = 0
        for item in cart_items:
            subtotal = float(item.finally_price)
            total += subtotal
            text += f'{item.product_name} - {item.quantity} шт. - {subtotal:.2f} BYN\n'
        text += f'\n💰 Общая сумма: {total:.2f} BYN\n\n'

        keyboard = cart_action_controller()
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "back_to_cart_review")
async def back_to_cart(callback: CallbackQuery):
    """Обработчик кнопки 'Назад' в корзине"""

    await callback.message.edit_text('Ваша корзина:', reply_markup=cart_action_controller())
    await callback.answer()
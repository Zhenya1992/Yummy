from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from config import MANAGER_ID
from database.models.users import Users

from bot_utils.message_utils import counting_products_from_cart

router = Router()


@router.callback_query(F.data == "Confirm_order")
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """Реакция на кнопку подтверждения заказа"""

    user = callback.from_user

    print(user, "*" * 150)
    phone = Users.phone
    print(phone)
    mention = f"<a href='tg://user?id={user.id}'>{user.full_name} </a>"
    user_text = f"Новый заказ от {mention}"
    context = counting_products_from_cart(user.id, user_text)
    print(context)


    if not context:
        await callback.message.edit_text('Корзина пуста, оформление заказа невозможно!')
        await callback.answer()
        return

    if not MANAGER_ID:
        await callback.message.edit_text("Менеджер не указан!")
        await callback.answer()
        return

    count, text, total_price, cart_id = context

    await bot.send_message(MANAGER_ID, text, parse_mode="HTML")

    await callback.message.edit_text("Ваш заказ принят! ✅ Ожидайте обратной связи от менеджера!")
    await callback.answer("Заказ оформлен! 🎉")

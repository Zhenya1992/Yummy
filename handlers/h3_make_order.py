from aiogram import Router, F, Bot
from aiogram.types import Message

from keyboards.inline_kb import show_category_menu
from keyboards.reply_kb import back_to_main_menu

router = Router()

@router.message(F.text == "Сделать заказ 📖")
async def make_order(message: Message, bot: Bot):
    """Обработчик реакции на кнопку 'Сделать заказ 📖'"""

    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Выберите из меню", reply_markup=back_to_main_menu())
    await message.answer(text="⬇️ Категории", reply_markup=show_category_menu(chat_id))

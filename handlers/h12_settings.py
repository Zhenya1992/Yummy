from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.utils import db_delete_user_by_telegram_id
from keyboards.inline_kb import show_settings_menu, delete_account_kb
from keyboards.reply_kb import get_main_menu, phone_button

router = Router()


@router.message(F.text == 'Настройки ⚙️')
async def handle_settings(message: Message):
    """Обработчик настроек"""

    await message.answer(text="Настройки 🖥️", reply_markup=show_settings_menu())


@router.callback_query(F.data == 'get_main_menu')
async def handle_main_menu(callback: CallbackQuery):
    """Обработчик кнопки Назад в настройках"""

    await callback.message.delete()
    await callback.message.answer('Главное меню 🏠', reply_markup=get_main_menu())


@router.callback_query(F.data == 'delete_account')
async def handle_delete_account(callback: CallbackQuery):
    """Обработчик кнопки Удалить аккаунт"""

    await callback.message.edit_text(text="Вы действительно хотите удалить аккаунт?", reply_markup=delete_account_kb())


@router.callback_query(F.data == 'delete_account_confirm')
async def handle_delete_account(callback: CallbackQuery):
    """Удаление аккаунта"""

    telegram_id = callback.from_user.id
    full_name = callback.from_user.full_name

    result = db_delete_user_by_telegram_id(telegram_id)

    if result:
        await callback.message.delete()

        await callback.message.answer(text=f"Аккаунт пользователя {full_name} успешно удален!", reply_markup=phone_button())

    else:
        await callback.message.edit_text("Ошибка при удалении аккаунта!", reply_markup=show_settings_menu())
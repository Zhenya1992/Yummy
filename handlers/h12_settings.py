from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from config import MANAGER_ID
from database.utils import db_delete_user_by_telegram_id, db_get_user_phone
from keyboards.inline_kb import show_settings_menu, delete_account_kb, open_instagram
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
async def handle_delete_account(callback: CallbackQuery, bot: Bot):
    """Удаление аккаунта"""

    telegram_id = callback.from_user.id
    full_name = callback.from_user.full_name
    phone = db_get_user_phone(telegram_id)

    result = db_delete_user_by_telegram_id(telegram_id)

    if result:
        await callback.message.delete()

        await callback.message.answer(
            text=f"Аккаунт пользователя {full_name} успешно удален!",
            reply_markup=phone_button())

        await callback.bot.send_message(
            MANAGER_ID,
            f'Пользователь {full_name}\n,с номером телефона {phone} удален!')
    else:
        await callback.message.edit_text("Ошибка при удалении аккаунта!", reply_markup=show_settings_menu())


@router.callback_query(F.data == 'show_settings')
async def handle_show_settings(callback: CallbackQuery):
    """Отмена удаления аккаунта"""

    await callback.message.delete()
    await callback.message.answer(
        text='Аккаунт не был удален!\nВы можете выбрать из меню⬇️',
        reply_markup=get_main_menu())


@router.callback_query(F.data == 'open_instagram')
async def handle_open_instagram(callback: CallbackQuery):
    """Открытие профиля в инстаграме"""

    await callback.message.edit_text(text='Вы хотите открыть профиль в инстаграме?', reply_markup=open_instagram())


@router.callback_query(F.data == 'get_settings_menu')
async def handle_get_settings_menu(callback: CallbackQuery):
    """Обработчик кнопки Назад в меню настроек"""

    await callback.message.edit_text(text='Назад в меню настроек ⬅️', reply_markup=show_settings_menu())
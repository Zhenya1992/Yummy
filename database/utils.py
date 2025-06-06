from sqlalchemy import update, select, join
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from database.base import engine
from database.models import Users, Carts, Categories, FinallyCarts

with Session(engine) as session:
    db_session = session


def db_register_user(full_name, chat_id, phone):
    """Регистрация юзеров в базе данных"""

    query = Users(name=full_name, telegram=chat_id, phone=phone)
    db_session.add(query)
    db_session.commit()


def db_is_registered(chat_id):
    """Проверка есть ли пользователь в базе данных"""

    user = db_session.execute(select(Users).where(Users.telegram == chat_id)).scalar_one_or_none()

    return bool(user)


def db_update_user(chat_id, phone: str):
    """Обновление данных юзера"""

    print(f"Обновляем {chat_id, phone}")
    query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
    db_session.execute(query)
    db_session.commit()


def db_create_user_cart(chat_id):
    """Создание корзины юзера в базе данных"""

    try:
        subquery = db_session.scalar(select(Users).where(Users.telegram == chat_id))
        query = Carts(user_id=subquery.id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        db_session.rollback()
    except AttributeError:
        db_session.rollback()


def db_get_all_categories():
    """Функция для получения всех категорий"""

    query = select(Categories)
    return db_session.scalars(query)


def db_get_finally_price(chat_id):
    """Получение итоговой цены"""

    query = select(func.sum(FinallyCarts.finally_price)).select_from(
        join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)).join(Users, Users.id == Carts.user_id).where(
        Users.telegram == chat_id)
    return db_session.execute(query).fetchone()[0]
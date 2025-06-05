from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.base import engine
from database.models import Users, Carts

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
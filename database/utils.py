from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.base import engine
from database.models import Users, Carts

with Session(engine) as session:
    db_session = session


def db_register_user(chat_id, full_name):
    """Регистрация юзеров в базе данных"""

    try:
        query = Users(name=full_name, telegram=chat_id)
        db_session.add(query)
        db_session.commit()
        return False
    except IntegrityError:
        db_session.rollback()
        return True


def db_update_user(chat_id, phone:str):
    """Обновление данных юзера"""

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
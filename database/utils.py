from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.base import engine
from database.models import Users

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
from sqlalchemy import update, select, join
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from database.base import engine
from database.models import Users, Carts, Categories, FinallyCarts, Products

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


def db_get_last_orders(chat_id, limit=5):
    """Получение 5 последних заказов пользователя"""

    query = (
        select(FinallyCarts).join(Carts, FinallyCarts.cart_id == Carts.id).
        join(Users, Users.id == Carts.user_id).
        where(Users.telegram == chat_id).order_by(FinallyCarts.id.desc()).limit(limit)
    )
    return db_session.scalars(query).all()


def db_get_products_from_category(category_id):
    """Получение товаров из категории"""

    query = (
        select(Products).where(Products.category_id == category_id)
    )

    return db_session.scalars(query)


def db_get_product_by_id(product_id):
    """Получение продукта по его ID"""

    query = (
        select(Products).where(Products.id == product_id)
    )
    return db_session.scalar(query)


def db_get_product_by_name(product_name):
    """Функция получения продукта по его имени"""

    query = (
        select(Products).where(Products.product_name == product_name)
    )
    return db_session.scalar(query)


def db_get_user_cart(chat_id):
    """Функция получения корзины пользователя по ID"""

    query = (
        select(Carts).join(Users).where(Users.telegram == chat_id)
    )
    return db_session.scalar(query)


def db_update_to_cart(price, cart_id, quantity=1):
    """Функция обновления корзины пользователя"""

    query = (
        update(Carts).where(Carts.id == cart_id).values(total_price=price, products=quantity)
    )
    db_session.execute(query)
    db_session.commit()



def db_upsert_to_finally_cart(cart_id, product_name, total_price, total_products):
    """Добавление и обновление товаров в итоговой корзине пользователя"""

    try:
        item = (
            db_session.query(FinallyCarts).filter_by(cart_id = cart_id, product_name = product_name)
        .first()
        )
        if item:
            item.quantity = total_products
            item.finally_price = total_price
            db_session.commit()
            return "Обновлено"

        new_item = FinallyCarts(
            cart_id = cart_id,
            product_name = product_name,
            quantity = total_products,
            finally_price = total_price,
        )

        db_session.add(new_item)
        db_session.commit()
        return "Добавлено"

    except Exception as e:
        print(e, "Ошибка при добавлении в итоговую корзину")
        return "Ошибка"


def db_get_cart_items(chat_id):
    """Получение товаров из корзины пользователя"""

    query = (
        select(FinallyCarts).join(Carts, FinallyCarts.cart_id == Carts.id).
        join(Users, Users.id == Carts.user_id).
        where(Users.telegram == chat_id)
    )
    return db_session.scalars(query).all()


def db_get_final_cart_items(chat_id):
    """"Получение товаров из итоговой корзины пользователя"""

    query = (
        select(FinallyCarts.product_name,
               FinallyCarts.quantity,
               FinallyCarts.finally_price,
               FinallyCarts.cart_id).
        join(Carts).join(Users).
        where(Users.telegram == chat_id)
    )
    return db_session.execute(query).fetchall()
from sqlalchemy.orm import Session
from sqlalchemy import text

from database.base import engine, Base
from database.models import Categories, Products


def create_db():
    """Функция создания базы данных"""

    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print("Создание базы данных 📗")

    Base.metadata.create_all(engine)

    categories = ("Торты" , "Зефир", "Пирожные")
    products = (
    ("Торты", "Медовик", 60, "нежный медовик", "media/cakes/cake1.jpg"),
    ("Торты", "Молочная девочка", 60, "воздушная молочная девочка", "media/cakes/cake2.jpg"),
    ("Торты", "Красный бархат", 60, "яркий красный бархат", "media/cakes/cake3.jpg"),
    ("Зефир", "Фрукто-ягодный", 20, "вкусный как облачко", "media/marshmallows/marshmallow1.jpg"),
    ("Зефир", "Кокосовый", 20, "обалденный", "media/marshmallows/marshmallow2.jpg"),
    ("Пирожные", "Медовый", 25, "ароматные", "media/pies/pie1.jpg"),
    ("Пирожные", "Вишня-шоколад", 25, "сытные", "media/pies/pie2.jpg"),
    )

    with Session(engine) as session:
        cats_map = {}

        for name in categories:
            category = Categories(category_name=name)
            session.add(category)
            session.flush()
            cats_map[name] = category.id

        for category_name, name, price, description, image in products:
            category_id = cats_map.get(category_name)
            if category_id:
                product = Products(
                    category_id = category_id,
                    product_name = name,
                    price = price,
                    description = description,
                    image = image
                )
                session.add(product)
        session.commit()
        print("С базой все: 👌")


if __name__ == "__main__":
    create_db()
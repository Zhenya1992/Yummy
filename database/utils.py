from sqlalchemy.orm import Session

from database.base import engine

with Session(engine) as session:
    db_session = session

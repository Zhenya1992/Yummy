from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DBUSER = getenv('DBUSER')
DBPASSWORD = getenv('DBPASSWORD')
DBADRESS = getenv('DBADRESS')
DBNAME = getenv('DBNAME')

DB_URL = f'postgresql://{DBUSER}:{DBPASSWORD}@{DBADRESS}/{DBNAME}'
engine = create_engine(DB_URL, echo=True)


class Base(DeclarativeBase):
    pass

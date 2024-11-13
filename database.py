import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

FSTR_DB_HOST = os.getenv('FSTR_DB_HOST')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT')
FSTR_DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.getenv('FSTR_DB_PASS')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME')

# print("FSTR_DB_HOST:", FSTR_DB_HOST)
# print("FSTR_DB_PORT:", FSTR_DB_PORT)
# print("FSTR_DB_LOGIN:", FSTR_DB_LOGIN)
# print("FSTR_DB_PASS:", FSTR_DB_PASS)
# print("FSTR_DB_NAME:", FSTR_DB_NAME)


DATABASE = f'postgresql://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{FSTR_DB_NAME}'

engine = create_engine(DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

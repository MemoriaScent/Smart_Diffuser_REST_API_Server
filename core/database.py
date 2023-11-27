from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
DATABASE_URL = f"mariadb+mariadbconnector://:{config.get('PASSWORD')}@{config.get('HOST')}:{config.get('PORT')}/{config.get('DATABASE')}"

# Craate Engin for mariadb
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

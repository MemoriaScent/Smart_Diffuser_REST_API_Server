from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
DATABASE_URL = f"mariadb:///?User={config.get('USER')}&Password={config.get('PASSWORD')}&Database={config.get('DATABASE')}&Server={config.get('HOST')}&Port={config.get('PORT')}"

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

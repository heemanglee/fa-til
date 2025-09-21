from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from common.config import get_settings

settings = get_settings()

DATABASE_URL = f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

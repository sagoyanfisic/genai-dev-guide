from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True if settings.environment == "development" else False,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
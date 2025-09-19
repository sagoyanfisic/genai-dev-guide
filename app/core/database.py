from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def create_database_engine():
    """Create database engine based on configuration"""
    # Use standard MySQL connection with public IP
    SQLALCHEMY_DATABASE_URL = settings.get_database_url()
    logger.info(f"🐬 Using MySQL connection: {SQLALCHEMY_DATABASE_URL}")

    return create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True if settings.environment == "development" else False,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
    )

engine = create_database_engine()

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
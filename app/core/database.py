from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def create_database_engine():
    """Create database engine based on configuration"""
    logger.info(f"Database configuration: USE_CLOUD_SQL={settings.use_cloud_sql}, USE_IAM_AUTH={settings.use_iam_auth}")
    logger.info(f"Cloud SQL Instance: {settings.cloud_sql_instance_connection_name}")
    logger.info(f"Cloud SQL IAM User: {settings.cloud_sql_iam_user}")

    if settings.use_cloud_sql:
        # Use Cloud SQL with Python Connector (for VPC and IAM auth)
        if not settings.cloud_sql_instance_connection_name:
            raise ValueError("CLOUD_SQL_INSTANCE_CONNECTION_NAME must be set when using Cloud SQL")

        from app.core.cloud_sql import create_cloud_sql_engine
        logger.info("🚀 Using Cloud SQL with Python Connector")
        return create_cloud_sql_engine()
    else:
        # Use standard MariaDB/MySQL connection
        SQLALCHEMY_DATABASE_URL = settings.get_database_url()
        logger.info(f"🐬 Using standard MariaDB connection: {SQLALCHEMY_DATABASE_URL}")

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
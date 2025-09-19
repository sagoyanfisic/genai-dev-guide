from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy.engine import Engine
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def create_cloud_sql_engine() -> Engine:
    """
    Create SQLAlchemy engine for Cloud SQL using the Cloud SQL Python Connector.
    This handles the connection to Cloud SQL instances in a VPC with IAM authentication.
    """
    if not settings.cloud_sql_instance_connection_name:
        raise ValueError("cloud_sql_instance_connection_name must be set when using Cloud SQL")

    def getconn():
        """Helper function to get database connection using Cloud SQL Connector"""
        connector = Connector()

        connection_params = {
            "instance_connection_string": settings.cloud_sql_instance_connection_name,
            "driver": "pymysql",
            "db": settings.db_name,
        }

        if settings.use_iam_auth:
            # Use IAM Database Authentication
            logger.info("Using IAM Database Authentication")
            if settings.cloud_sql_iam_user:
                connection_params["user"] = settings.cloud_sql_iam_user
            else:
                # Use the service account identity from the runtime environment
                connection_params["user"] = settings.db_user

            # Enable IAM authentication
            connection_params["enable_iam_auth"] = True
        else:
            # Use traditional username/password authentication
            logger.info("Using traditional username/password authentication")
            connection_params["user"] = settings.db_user
            connection_params["password"] = settings.db_password

        conn = connector.connect(**connection_params)
        return conn

    # Create the SQLAlchemy engine using the connection function
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        echo=True if settings.environment == "development" else False,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
    )

    auth_method = "IAM" if settings.use_iam_auth else "username/password"
    logger.info(f"Created Cloud SQL engine for instance: {settings.cloud_sql_instance_connection_name} using {auth_method} authentication")
    return engine


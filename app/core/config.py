from pydantic_settings import BaseSettings
from typing import Optional
import os
from .secret_manager import get_secret_or_env

class Settings(BaseSettings):
    google_api_key: str
    database_url: Optional[str] = None  # Optional - not used for Cloud SQL
    db_host: str = "mariadb"
    db_port: int = 3306
    db_name: str = "pdf_ai_db"
    db_user: str = "pdf_user"
    db_password: str = "pdf_password"
    environment: str = "development"
    gcp_project_id: Optional[str] = None

    # Cloud SQL Configuration
    use_cloud_sql: bool = False
    cloud_sql_instance_connection_name: Optional[str] = None

    # IAM Database Authentication
    use_iam_auth: bool = False
    cloud_sql_iam_user: Optional[str] = None  # Service account email for IAM auth
    
    # AI Service Configuration - Only Gemini Direct API
    use_vertex_ai: bool = False  # Forced to False - only Gemini Direct allowed
    
    # Security Configuration
    cors_origins: Optional[str] = None
    
    class Config:
        env_file = ".env"

    def get_google_api_key(self) -> str:
        """Get Google API key lazily"""
        if not hasattr(self, '_google_api_key'):
            self._google_api_key = (
                get_secret_or_env("google-api-key", "GOOGLE_API_KEY") or 
                self.google_api_key or 
                os.getenv("GOOGLE_API_KEY", "")
            )
        return self._google_api_key
    
    def get_database_url(self) -> str:
        """Get database URL for local MariaDB connection"""
        # Only used for local MariaDB - Cloud SQL uses the Python Connector
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
from pydantic_settings import BaseSettings
from typing import Optional
import os
from .secret_manager import get_secret_or_env, get_database_config_from_secret

class Settings(BaseSettings):
    google_api_key: Optional[str] = None
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load database config from secret if available
        self._load_database_config_from_secret()

    def _load_database_config_from_secret(self):
        """Load database configuration from GCP Secret Manager"""
        db_config = get_database_config_from_secret()
        if db_config:
            # Update from secret, environment variables already loaded by Pydantic
            self.db_host = db_config.get("DB_HOST", self.db_host)
            self.db_port = db_config.get("DB_PORT", self.db_port)
            self.db_name = db_config.get("DB_NAME", self.db_name)
            self.db_user = db_config.get("DB_USER", self.db_user)
            self.db_password = db_config.get("DB_PASSWORD", self.db_password)
            self.use_cloud_sql = db_config.get("USE_CLOUD_SQL", self.use_cloud_sql)

    def get_google_api_key(self) -> str:
        """Get Google API key lazily"""
        if not hasattr(self, '_google_api_key'):
            api_key = (
                get_secret_or_env("google-api-key", "GOOGLE_API_KEY") or
                self.google_api_key or
                os.getenv("GOOGLE_API_KEY", "")
            )
            if not api_key:
                raise ValueError(
                    "Google API key is required but not found. Set GOOGLE_API_KEY environment variable "
                    "or configure google-api-key in Google Secret Manager."
                )
            self._google_api_key = api_key
        return self._google_api_key
    
    def get_database_url(self) -> str:
        """Get database URL for MariaDB connection"""
        # MariaDB connection using MySQL protocol
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
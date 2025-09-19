import os
import json
from typing import Optional, Dict, Any
from google.cloud import secretmanager
import logging

logger = logging.getLogger(__name__)

def get_secret_or_env(secret_name: str, fallback_env_name: Optional[str] = None) -> Optional[str]:
    fallback_name = fallback_env_name or secret_name
    
    try:
        project_id = os.getenv('GCP_PROJECT_ID')
        if not project_id:
            return os.getenv(fallback_name)
        
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
        
    except Exception as e:
        logger.warning(f"Failed to get secret {secret_name}: {e}, using env var")
        return os.getenv(fallback_name)

def get_database_config_from_secret() -> Optional[Dict[str, Any]]:
    try:
        project_id = os.getenv('GCP_PROJECT_ID')
        if not project_id:
            logger.info("No GCP_PROJECT_ID found, using environment variables")
            return None

        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/{project_id}/secrets/develop_poc-database/versions/latest"
        response = client.access_secret_version(request={"name": secret_name})
        secret_data = response.payload.data.decode("UTF-8")

        config = json.loads(secret_data)
        logger.info("Successfully loaded database config from secret manager")
        return config

    except Exception as e:
        logger.warning(f"Failed to get database config from secret: {e}, using environment variables")
        return None
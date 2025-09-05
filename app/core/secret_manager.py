import os
from typing import Optional
from google.cloud import secretmanager
import logging

logger = logging.getLogger(__name__)

def get_secret_or_env(secret_name: str, fallback_env_name: Optional[str] = None) -> Optional[str]:
    """
    Intenta obtener un secret de GCP Secret Manager, si falla usa variables de entorno
    """
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
from google.cloud import secretmanager
from google.cloud.secretmanager_v1beta2 import SecretManagerServiceClient
from google.api_core.exceptions import NotFound, PermissionDenied, GoogleAPIError
from google.auth.credentials import Credentials

from config import GOOGLE_PROJECT_ID, GEMINI_KEY_ID, GOOGLE_SERVICE_ACCOUNT_CRED_B64, MISTRAL_KEY_ID
from google.oauth2 import service_account
import logging
from base64 import b64decode
import json


logger = logging.getLogger("app")

def load_credentials() -> Credentials:
    """Load credentials from the service account key file."""
    try:
        if not GOOGLE_SERVICE_ACCOUNT_CRED_B64:
            raise ValueError("Service account credentials path is not configured.")
        
        creds = json.loads(b64decode(GOOGLE_SERVICE_ACCOUNT_CRED_B64))

        g_credentials = service_account.Credentials.from_service_account_info(creds)
        logger.info("Successfully loaded service account credentials.")
        return g_credentials
    except FileNotFoundError as e:
        logger.error(f"Service account credentials file not found: {e}")
        raise
    except ValueError as ve:
        logger.error(f"Configuration error: {ve}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading credentials: {e}")
        raise


def initialize_secret_manager_client(g_credentials: Credentials) -> SecretManagerServiceClient:
    """Create and return a Secret Manager client with the provided credentials."""
    try:
        g_client = secretmanager.SecretManagerServiceClient(credentials=g_credentials)
        logger.info("Successfully initialized Secret Manager client.")
        return g_client
    except Exception as e:
        logger.error(f"Failed to initialize Secret Manager client: {e}")
        raise


def get_secret(g_client, secret_id, version="latest"):
    """
    Fetch a secret from Google Secret Manager.

    Args:
        g_client (SecretManagerServiceClient): The Secret Manager client.
        secret_id (str): The ID of the secret to retrieve.
        version (str): The version of the secret (default is 'latest').

    Returns:
        str: The secret value as a string.

    Raises:
        ValueError: If the secret ID is not configured.
        Exception: If accessing the secret fails.
    """
    try:
        if not GOOGLE_PROJECT_ID:
            raise ValueError("Google Project ID is not configured.")
        if not secret_id:
            raise ValueError("Secret ID is not provided.")

        # Build the resource name of the secret version
        name = f"projects/{GOOGLE_PROJECT_ID}/secrets/{secret_id}/versions/{version}"

        # Access the secret
        response = g_client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        logger.info(f"Successfully accessed secret: {secret_id}")
        return secret_value
    except ValueError as ve:
        logger.error(f"Configuration error: {ve}")
        raise
    except NotFound as e:
        logger.error(f"Secret not found: {secret_id} - {e}")
        raise
    except PermissionDenied as e:
        logger.error(f"Permission denied when accessing secret: {secret_id} - {e}")
        raise
    except GoogleAPIError as e:
        logger.error(f"API error while accessing secret {secret_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while accessing secret {secret_id}: {e}")
        raise


# Orchestrate the process
try:
    credentials = load_credentials()
    client = initialize_secret_manager_client(credentials)
    GEMINI_KEY = get_secret(client, GEMINI_KEY_ID)
    MISTRAL_KEY = get_secret(client, MISTRAL_KEY_ID)
    logger.info("Successfully retrieved API keys.")
except Exception as ex:
    logger.error(f"Failed to retrieve API keys: {ex}")
    GEMINI_KEY = None
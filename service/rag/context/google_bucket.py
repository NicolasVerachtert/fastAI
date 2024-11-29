from google.cloud import storage

from config import GOOGLE_SERVICE_ACCOUNT_CRED_B64, GCS_BUCKET_NAME, GCS_DOCS_PATH, DOCS_PATH
import logging
import os
import json
from base64 import b64decode


logger = logging.getLogger("app")


def validate_config():
    """Validates required configurations."""
    if not GOOGLE_SERVICE_ACCOUNT_CRED_B64:
        logger.error("Google service account credential path is not configured.")
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_CRED_PATH is not configured.")
    if not GCS_BUCKET_NAME:
        logger.error("GCS bucket name is not configured.")
        raise ValueError("GCS_BUCKET_NAME is not configured.")
    if not GCS_DOCS_PATH:
        logger.error("GCS documents path is not configured.")
        raise ValueError("GCS_DOCS_PATH is not configured.")
    if not DOCS_PATH:
        logger.error("Local documents path is not configured.")
        raise ValueError("DOCS_PATH is not configured.")


def initialize_gcs_client() -> storage.Client:
    """Initializes and returns the Google Cloud Storage client."""
    try:

        creds = json.loads(b64decode(GOOGLE_SERVICE_ACCOUNT_CRED_B64))
        client = storage.Client.from_service_account_info(creds)
        logger.info("Successfully initialized Google Cloud Storage client.")
        
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {e}")
        raise


def get_gcs_bucket(client: storage.Client) -> storage.Bucket:
    """Retrieves the GCS bucket."""
    try:
        bucket = client.bucket(GCS_BUCKET_NAME)
        logger.info(f"Successfully connected to GCS bucket: {GCS_BUCKET_NAME}")
        return bucket
    except Exception as e:
        logger.error(f"Failed to access GCS bucket {GCS_BUCKET_NAME}: {e}")
        raise


def ensure_local_directory():
    """Ensures the local directory for downloads exists."""
    try:
        if not os.path.exists(DOCS_PATH):
            os.makedirs(DOCS_PATH)
            logger.info(f"Created local directory: {DOCS_PATH}")
    except OSError as e:
        logger.error(f"Failed to create local directory {DOCS_PATH}: {e}")
        raise


def download_blob(blob: storage.Blob, gcs_docs_path: str) -> None:
    """Downloads a single blob, flattening folder structure."""
    try:
        # Skip folder objects (blobs that represent folders end with '/')
        if blob.name.endswith('/'):
            logger.debug(f"Skipping folder: {blob.name}")
            return

        # Extract the file name and handle subfolder structure
        file_name = os.path.basename(blob.name)
        if '/' in blob.name[len(gcs_docs_path):]:
            subfolder_name = blob.name[len(gcs_docs_path):].split('/')[0]
            file_name = f"{subfolder_name}_{file_name}"

        # Define the local file path
        local_file_path = os.path.join(DOCS_PATH, file_name)

        # Download the file
        blob.download_to_filename(local_file_path)
        logger.info(f"Downloaded {file_name} to {local_file_path}")
    except Exception as e:
        logger.error(f"Failed to download blob {blob.name}: {e}")


def download_files_from_gcs() -> None:
    """
    Downloads files from a GCS folder to a local directory, flattening the folder structure.
    """
    # Step 1: Validate configuration
    validate_config()

    # Step 2: Initialize GCS client and bucket
    client = initialize_gcs_client()
    bucket = get_gcs_bucket(client)

    # Step 3: Ensure local directory exists
    ensure_local_directory()

    # Step 4: List and download files
    blobs = bucket.list_blobs(prefix=GCS_DOCS_PATH)
    gcs_folder_path = GCS_DOCS_PATH if GCS_DOCS_PATH.endswith('/') else GCS_DOCS_PATH + '/'

    for blob in blobs:
        download_blob(blob, gcs_folder_path)

    logger.info("Completed fetching files from GCS bucket.")
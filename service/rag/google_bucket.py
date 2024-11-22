from google.cloud import storage

from config import GOOGLE_SERVICE_ACCOUNT_CRED_PATH, GCS_BUCKET_NAME, GCS_DOCS_PATH, DOCS_PATH
import logging
import os

logger = logging.getLogger("app")

def download_files_from_gcs() -> None:
    """
    Downloads files from a GCS folder to a local directory, flattening the folder structure.
    
    This function connects to Google Cloud Storage, lists all the files under the specified
    folder path in the GCS bucket, and downloads them to a local directory. If files are inside
    subfolders in GCS, their names will be modified by prepending the subfolder's name to 
    avoid conflicts and preserve some structure in the local directory.
    
    Returns:
        None
    """
    
    logger.info("Fetching all files from bucket...")
    
    client = storage.Client.from_service_account_json(GOOGLE_SERVICE_ACCOUNT_CRED_PATH)
    bucket = client.bucket(GCS_BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=GCS_DOCS_PATH)

    # Create the local directory if it does not exist
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)
        logger.info(f"Created local directory: {DOCS_PATH}")

    # Iterate over the blobs and download them
    for blob in blobs:
        # Skip folder objects (blobs that represent folders end with a '/')
        if blob.name.endswith('/'):
            continue
        
        # Extract the file name from the blob's name
        file_name = os.path.basename(blob.name)
       
        gcs_folder_path = GCS_DOCS_PATH if  GCS_DOCS_PATH.endswith('/') else GCS_DOCS_PATH + '/'

        # If the file is inside a subfolder, prepend the subfolder name to the file name
        if '/' in blob.name[len(gcs_folder_path):]:
            subfolder_name = blob.name[len(gcs_folder_path):].split('/')[0]
            file_name = f"{subfolder_name}_{file_name}"

        # Define the local file path to store the downloaded file
        local_file_path = os.path.join(DOCS_PATH, file_name)

        # Download the file from GCS to the local path
        blob.download_to_filename(local_file_path)
        logger.info(f"Downloaded {file_name} to {local_file_path}")
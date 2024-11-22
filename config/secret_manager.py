from google.cloud import secretmanager
from config import GOOGLE_PROJECT_ID, GOOGLE_GEMINI_KEY_ID, GOOGLE_SERVICE_ACCOUNT_CRED_PATH
from google.oauth2 import service_account

# Load credentials from the service account key file
credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_CRED_PATH)

# Create the Secret Manager client with the credentials
client = secretmanager.SecretManagerServiceClient(credentials=credentials)

# Build the resource name of the secret version
def get_secret(secret_id, version="latest"):
    """Fetch a secret from Google Secret Manager."""
    name = f"projects/{GOOGLE_PROJECT_ID}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Access the Gemini API key
GEMINI_KEY = get_secret(GOOGLE_GEMINI_KEY_ID)
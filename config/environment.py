from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Application configuration
DATA_PATH = os.getenv("DATA_FOLDER", "data")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
GEMINI_LLM_MODEL = os.getenv("GEMINI_LLM_MODEL", "gemini-1.5-flash-latest")

# Server configuration
UVICORN_PORT = int(os.getenv("UVICORN_PORT", 5000))
UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")

# Path configuration
CHROMA_PATH = f"{DATA_PATH}/chroma"
DOCS_PATH = f"{DATA_PATH}/docs"

# Google Cloud configuration
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "integratieproject-2-442110")
GOOGLE_GEMINI_KEY_ID = os.getenv("GOOGLE_GEMINI_KEY_ID", "GEMINI_API_KEY")
GOOGLE_SERVICE_ACCOUNT_CRED_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_CRED_PATH", "credentials.json")
GCS_BUCKET_NAME=os.getenv("GCS_BUCKET_NAME", "team-20-monopoly-ip2-media-bucket")
GCS_DOCS_PATH = os.getenv("GCS_DOCS_PATH", "monopoly-user-guides")
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Required
GOOGLE_SERVICE_ACCOUNT_CRED_B64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_CRED_B64")

# Application configuration
DATA_PATH = os.getenv("DATA_FOLDER", "data")

# Server configuration
UVICORN_PORT = int(os.getenv("UVICORN_PORT", 5000))
UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")

# Path configuration
CHROMA_PATH = f"{DATA_PATH}{os.sep}chroma"
DOCS_PATH = f"{DATA_PATH}{os.sep}docs"
CHROMA_RESET = bool(os.getenv("CRHOMA_RESET", "false"))

# Google Cloud configuration
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "integratieproject-2-442110")

GCS_BUCKET_NAME=os.getenv("GCS_BUCKET_NAME", "team-20-monopoly-ip2-media-bucket")
GCS_DOCS_PATH = os.getenv("GCS_DOCS_PATH", "monopoly-user-guides")

# Gemini AI configuration
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
GEMINI_LLM_MODEL = os.getenv("GEMINI_LLM_MODEL", "gemini-1.5-flash-latest")
GEMINI_KEY_ID = os.getenv("GOOGLE_GEMINI_KEY_ID", "GEMINI_API_KEY")

# Mistral AI configuration
MISTRAL_KEY_ID = os.getenv("MISTRAL_KEY_ID", "MISTRAL_API_KEY")
MISTRAL_LLM_MODEL = os.getenv("MISTRAL_LLM_MODEL", "open-mistral-7b")

# Artifacts for Prediction Model
ARTIFACTS_PATH = os.getenv("ARTIFACTS_PATH", "artifacts")
PREDICTION_ARTIFACTS_PATH = os.getenv("PREDICTION_ARTIFACTS_PATH", f"{ARTIFACTS_PATH}{os.sep}prediction_model")
import os

from dotenv import load_dotenv

load_dotenv()

DATA_PATH = os.getenv('DATA_FOLDER', "data")
GEMINI_KEY = os.getenv('GEMINI_KEY', "Default_key")
GEMINI_EMBED_MODEL = os.getenv('GEMINI_EMBEDDING_MODEL', "models/embedding-001")
GEMINI_LLM_MODEL = os.getenv('GEMINI_LLM_MODEL', "gemini-1.5-flash-latest")
UVICORN_PORT = int(os.getenv('UVICORN_PORT', 5000))
UVICORN_HOST = os.getenv('UVICORN_HOST', "0.0.0.0")
CHROMA_PATH = f"{DATA_PATH}/chroma"
DOCS_PATH = f"{DATA_PATH}/docs"
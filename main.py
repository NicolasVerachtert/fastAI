import uvicorn
from fastapi import FastAPI
from api import chatbox_api
from service.rag import init_chroma, download_files_from_gcs
from config import UVICORN_PORT, UVICORN_HOST, setup_logging, LOGGING_CONFIG

def setup_app() -> None:
    """Setup FastAPI app"""
    setup_logging()
    
def load_rag() -> None:
    """Load Rag model and initialise chroma"""
    download_files_from_gcs()
    init_chroma(reset=False)


if __name__ == "__main__":
    
    setup_app()
    load_rag()
    
    
    app = FastAPI()
    app.include_router(chatbox_api.router)
    
    
    uvicorn.run(
        app,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        log_config=LOGGING_CONFIG
    )
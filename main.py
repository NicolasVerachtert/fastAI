import uvicorn
from fastapi import FastAPI
from api import chatbot, prediction
from config import UVICORN_PORT, UVICORN_HOST, setup_logging, LOGGING_CONFIG
from db import init_db


def setup_app() -> None:
    """Setup FastAPI app"""
    
    setup_logging()


if __name__ == "__main__":
    setup_app()
    init_db()

    app = FastAPI()
    app.include_router(chatbot.router)
    app.include_router(prediction.router)

    uvicorn.run(
        app,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        log_config=LOGGING_CONFIG
    )

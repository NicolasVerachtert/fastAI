import uvicorn
from fastapi import FastAPI
from api import chatbox_api
from service.rag import init_chroma
from config import UVICORN_PORT, UVICORN_HOST



if __name__ == "__main__":
    app = FastAPI()
    app.include_router(chatbox_api.router)

    init_chroma(reset=False)
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)
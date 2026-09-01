import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.game_router import router
from app.api.websocket_router import router as websocket_router
from app.api.exception_handlers import (
    register_exception_handlers,
)

app = FastAPI()

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://minesweeper-pvp-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(router)
app.include_router(websocket_router)


@app.get("/")
def root():
    return {
        "message": "Minesweeper API",
    }
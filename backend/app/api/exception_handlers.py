from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    CellAlreadyOpenedError,
    CellFlaggedError,
    GameNotFoundError,
)

def register_exception_handlers(app):

    @app.exception_handler(GameNotFoundError)
    async def game_not_found(
        request: Request,
        exc: GameNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(CellFlaggedError)
    async def flagged(
        request: Request,
        exc: CellFlaggedError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(CellAlreadyOpenedError)
    async def opened(
        request: Request,
        exc: CellAlreadyOpenedError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )
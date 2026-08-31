from fastapi import APIRouter, WebSocket

from app.websocket.connection_manager import (
    manager,
)


router = APIRouter()


@router.websocket("/games/{game_id}/ws")
async def game_websocket(
    websocket: WebSocket,
    game_id: str,
):
    await manager.connect(
        game_id,
        websocket,
    )

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        manager.disconnect(
            game_id,
            websocket,
        )
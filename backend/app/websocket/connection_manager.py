import json

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.connections: dict[
            str,
            list[WebSocket],
        ] = {}

    async def connect(
        self,
        game_id: str,
        websocket: WebSocket,
    ) -> None:
        await websocket.accept()

        if game_id not in self.connections:
            self.connections[game_id] = []

        self.connections[game_id].append(
            websocket,
        )

    def disconnect(
        self,
        game_id: str,
        websocket: WebSocket,
    ) -> None:
        if game_id not in self.connections:
            return

        if websocket in self.connections[game_id]:
            self.connections[game_id].remove(
                websocket,
            )

        if not self.connections[game_id]:
            del self.connections[game_id]

    async def broadcast(
        self,
        game_id: str,
        message: str,
    ) -> None:
        if game_id not in self.connections:
            return

        for websocket in self.connections[game_id]:
            await websocket.send_text(message)

    async def broadcast_json(
        self,
        game_id: str,
        message: dict,
    ) -> None:
        if game_id not in self.connections:
            return

        message_json = json.dumps(message)

        for websocket in self.connections[game_id]:
            await websocket.send_text(
                message_json,
            )


manager = ConnectionManager()
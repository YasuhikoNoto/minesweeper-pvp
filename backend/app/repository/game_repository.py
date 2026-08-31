from uuid import uuid4

from app.domain.game import Game
from app.domain.exceptions import GameNotFoundError

class GameRepository:
    def __init__(self):
        self._games: dict[str, Game] = {}

    def save(
        self,
        game: Game
    ) -> str:
        game_id = str(uuid4())

        self._games[game_id] = game

        return game_id

    def find_by_id(
        self,
        game_id: str
    ) -> Game:
        game = self._games.get(game_id)

        if game is None:
            raise GameNotFoundError()

        return game

    def update(
        self,
        game_id: str,
        game: Game,
    ) -> None:
        self._games[game_id] = game
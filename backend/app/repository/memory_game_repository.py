from uuid import uuid4

from app.domain.exceptions import GameNotFoundError
from app.domain.game import Game

from .game_repository import GameRepository


class MemoryGameRepository(GameRepository):

    def __init__(self):
        self.games: dict[str, Game] = {}

    def save(self, game: Game) -> str:
        game_id = str(uuid4())

        self.games[game_id] = game

        return game_id

    def find_by_id(self, game_id: str) -> Game:
        game = self.games.get(game_id)

        if game is None:
            raise GameNotFoundError()

        return game

    def update(
        self,
        game_id: str,
        game: Game,
    ) -> None:
        self.games[game_id] = game
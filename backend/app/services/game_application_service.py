from app.domain.game import Game
from app.domain.game_status import GameStatus
from app.domain.player import Player
from app.domain.position import Position
from app.repository.game_repository import GameRepository
from app.services.game_service import GameService


class GameApplicationService:

    def __init__(
        self,
        repository: GameRepository,
        game_service: GameService,
    ):
        self.repository = repository
        self.game_service = game_service

    def create_game(
        self,
        width: int,
        height: int,
        mine_count: int,
        player_id: str,
    ) -> str:

        game = Game(
            width=width,
            height=height,
            mine_count=mine_count,
        )

        game.add_player(
            Player(id=player_id),
        )

        return self.repository.save(game)

    def join_game(
        self,
        game_id: str,
        player_id: str,
    ) -> Player:

        game = self.repository.find_by_id(game_id)

        player = Player(
            id=player_id,
        )

        game.add_player(player)

        self.repository.update(
            game_id,
            game,
        )

        return player

    def start_game(
        self,
        game_id: str,
    ) -> Game:

        game = self.repository.find_by_id(game_id)

        self.game_service.start(game)

        self.repository.update(
            game_id,
            game,
        )

        return game

    def open_cell(
        self,
        game_id: str,
        position: Position,
        player_id: str,
    ) -> Game:

        game = self.repository.find_by_id(game_id)

        self.game_service.open(
            game,
            position,
            player_id,
        )

        self.repository.update(
            game_id,
            game,
        )

        return game

    def toggle_flag(
        self,
        game_id: str,
        position: Position,
        player_id: str,
    ) -> Game:

        game = self.repository.find_by_id(game_id)

        self.game_service.toggle_flag(
            game,
            position,
            player_id,
        )

        self.repository.update(
            game_id,
            game,
        )

        return game

    def find_game(
        self,
        game_id: str,
    ) -> Game:

        return self.repository.find_by_id(
            game_id,
        )

    def rematch_game(
        self,
        game_id: str,
        player_id: str,
    ) -> str:

        old_game = self.repository.find_by_id(
            game_id,
        )

        if old_game.status not in (
            GameStatus.GAME_OVER,
            GameStatus.CLEAR,
        ):
            raise ValueError(
                "終了したゲームのみ再戦できます。"
            )

        if not any(
            player.id == player_id
            for player in old_game.players
        ):
            raise ValueError(
                "このゲームのプレイヤーではありません。"
            )

        new_game = Game(
            width=old_game.width,
            height=old_game.height,
            mine_count=old_game.mine_count,
        )

        for player in old_game.players:
            new_game.add_player(
                Player(id=player.id),
            )

        return self.repository.save(
            new_game,
        )
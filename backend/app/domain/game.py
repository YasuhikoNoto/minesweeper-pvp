from dataclasses import dataclass, field

from app.domain.board import Board
from app.domain.game_status import GameStatus
from app.domain.player import Player


@dataclass
class Game:
    width: int
    height: int
    mine_count: int

    board: Board = field(init=False)

    status: GameStatus = GameStatus.NOT_STARTED

    players: list[Player] = field(default_factory=list)

    current_player_id: str | None = None

    winner_player_id: str | None = None

    mines_generated: bool = False

    def __post_init__(self):
        self.board = Board(self.width, self.height)

    def add_player(self, player: Player) -> None:
        if player in self.players:
            raise ValueError(
                "このプレイヤーはすでに参加しています。"
            )

        if len(self.players) >= 2:
            raise ValueError(
                "これ以上プレイヤーを追加できません。"
            )

        self.players.append(player)

    def start(self) -> None:
        if self.status != GameStatus.NOT_STARTED:
            raise ValueError(
                "ゲームは開始できる状態ではありません。"
            )

        if len(self.players) < 2:
            raise ValueError(
                "プレイヤーが2人揃っていません。"
            )

        self.status = GameStatus.PLAYING
        self.current_player_id = self.players[0].id
        self.winner_player_id = None

    def is_current_player(
        self,
        player_id: str,
    ) -> bool:
        return self.current_player_id == player_id

    def switch_turn(self) -> None:
        if len(self.players) != 2:
            raise ValueError(
                "ターンを交代するにはプレイヤーが2人必要です。"
            )

        if self.current_player_id == self.players[0].id:
            self.current_player_id = self.players[1].id
            return

        if self.current_player_id == self.players[1].id:
            self.current_player_id = self.players[0].id
            return

        raise ValueError(
            "現在のプレイヤーが設定されていません。"
        )

    def set_winner_by_losing_player(
        self,
        losing_player_id: str,
    ) -> None:
        for player in self.players:
            if player.id != losing_player_id:
                self.winner_player_id = player.id
                return

        raise ValueError(
            "敗北したプレイヤー以外のプレイヤーが存在しません。"
        )
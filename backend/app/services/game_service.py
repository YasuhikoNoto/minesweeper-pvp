from app.domain.flood_fill_service import FloodFillService
from app.domain.game import Game
from app.domain.game_status import GameStatus
from app.domain.judge_service import JudgeService
from app.domain.mine_generator import MineGenerator
from app.domain.number_calculator import NumberCalculator
from app.domain.position import Position
from app.domain.exceptions import (
    CellAlreadyOpenedError,
    CellFlaggedError,
)


class GameService:

    def __init__(
        self,
        mine_generator: MineGenerator,
        number_calculator: NumberCalculator,
        flood_fill_service: FloodFillService,
        judge_service: JudgeService,
    ):
        self.mine_generator = mine_generator
        self.number_calculator = number_calculator
        self.flood_fill_service = flood_fill_service
        self.judge_service = judge_service

    def start(self, game: Game) -> None:
        game.start()

    def open(
        self,
        game: Game,
        position: Position,
        player_id: str,
    ) -> None:

        if game.status in (
            GameStatus.GAME_OVER,
            GameStatus.CLEAR,
        ):
            return

        if game.status != GameStatus.PLAYING:
            raise ValueError(
                "ゲームが開始されていません。"
            )

        if not game.is_current_player(player_id):
            raise ValueError(
                "現在のターンではありません。"
            )

        cell = game.board.get_cell(position)

        if (
            cell.is_flagged
            and cell.flagged_by == player_id
        ):
            raise CellFlaggedError(
                "自分がFlagしたセルは開けません。"
            )

        if not game.mines_generated:

            self.mine_generator.generate(
                game.board,
                game.mine_count,
                safe_position=position,
            )

            self.number_calculator.calculate(
                game.board,
            )

            game.mines_generated = True

        self.flood_fill_service.open(
            game.board,
            position,
            player_id,
        )

        if cell.is_mine:
            game.status = GameStatus.GAME_OVER
            game.set_winner_by_losing_player(player_id)
            return

        if self.judge_service.is_clear(game.board):
            game.status = GameStatus.CLEAR
            game.winner_player_id = None
            return

        game.switch_turn()

    def toggle_flag(
        self,
        game: Game,
        position: Position,
        player_id: str,
    ) -> None:

        if game.status in (
            GameStatus.GAME_OVER,
            GameStatus.CLEAR,
        ):
            return

        if game.status != GameStatus.PLAYING:
            raise ValueError(
                "ゲームが開始されていません。"
            )

        cell = game.board.get_cell(position)

        if cell.is_open:
            raise CellAlreadyOpenedError(
                "開いているセルにはフラグを立てられません。"
            )

        if not game.is_current_player(player_id):
            raise ValueError(
                "現在のターンではありません。"
            )

        cell.toggle_flag(player_id)
from app.api.schemas import (
    BoardResponse,
    CellResponse,
    GameResponse,
)
from app.domain.game import Game
from app.domain.game_status import GameStatus


class GameMapper:

    @staticmethod
    def to_response(
        game_id: str,
        game: Game,
        player_id: str,
    ) -> GameResponse:

        cells = [
            [
                CellResponse(
                    x=cell.position.x,
                    y=cell.position.y,
                    is_open=(
                        cell.is_open
                        and cell.opened_by == player_id
                    ),
                    is_opened_by_opponent=(
                        cell.is_open
                        and cell.opened_by != player_id
                    ),
                    is_mine=(
                        cell.is_mine
                        if (
                            game.status in (
                                GameStatus.GAME_OVER,
                                GameStatus.CLEAR,
                            )
                            or (
                                cell.is_open
                                and cell.opened_by == player_id
                            )
                        )
                        else False
                    ),
                    is_flagged=cell.is_flagged,
                    adjacent_mines=(
                        cell.adjacent_mines
                        if (
                            cell.is_open
                            and cell.opened_by == player_id
                        )
                        else None
                    ),
                )
                for cell in row
            ]
            for row in game.board.cells
        ]

        return GameResponse(
            game_id=game_id,
            width=game.board.width,
            height=game.board.height,
            mine_count=game.mine_count,
            status=game.status.value,
            current_player_id=game.current_player_id,
            winner_player_id=game.winner_player_id,
            board=BoardResponse(
                width=game.board.width,
                height=game.board.height,
                cells=cells,
            ),
        )
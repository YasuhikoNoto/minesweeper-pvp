from dataclasses import dataclass

from .exceptions import (
    CellAlreadyOpenedError,
    CellFlaggedError,
)
from .position import Position


@dataclass
class Cell:
    position: Position

    is_mine: bool = False
    is_open: bool = False
    is_flagged: bool = False
    flagged_by: str | None = None
    adjacent_mines: int = 0
    opened_by: str | None = None

    def open(self, player_id: str) -> None:

        if self.is_open:
            raise CellAlreadyOpenedError(
                "すでに開いているセルです。"
            )

        if self.flagged_by == player_id:
            raise CellFlaggedError(
                "自分がFlagしたセルは開けません。"
            )

        if self.flagged_by is not None:
            self.is_flagged = False
            self.flagged_by = None

        self.is_open = True
        self.opened_by = player_id

    def toggle_flag(self, player_id: str) -> None:

        if self.is_open:
            raise CellAlreadyOpenedError(
                "開いているセルにはフラグを立てられません。"
            )

        if self.flagged_by == player_id:
            self.is_flagged = False
            self.flagged_by = None
            return

        self.is_flagged = True
        self.flagged_by = player_id
from .board import Board
from .position import Position


class NumberCalculator:
    """
    各セルの周囲の地雷数を計算する
    """

    def calculate(self, board: Board) -> None:

        for row in board.cells:
            for cell in row:

                if cell.is_mine:
                    continue

                count = sum(
                    1
                    for neighbor in board.neighbors(cell.position)
                    if neighbor.is_mine
                )

                cell.adjacent_mines = count
import random

from .board import Board
from .position import Position


class MineGenerator:

    def generate(
        self,
        board: Board,
        mine_count: int,
        safe_position: Position,
    ) -> None:

        if mine_count >= board.width * board.height:
            raise ValueError(
                "地雷が多すぎます。"
            )

        candidates: list[Position] = []

        for y in range(board.height):
            for x in range(board.width):

                position = Position(
                    x=x,
                    y=y,
                )

                if position == safe_position:
                    continue

                candidates.append(position)

        positions = random.sample(
            candidates,
            mine_count,
        )

        for position in positions:
            board.get_cell(position).is_mine = True
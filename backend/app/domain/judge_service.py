from .board import Board


class JudgeService:

    def is_clear(self, board: Board) -> bool:
        """
        全ての安全マスが開いているか判定する
        """

        for row in board.cells:
            for cell in row:

                if cell.is_mine:
                    continue

                if not cell.is_open:
                    return False

        return True
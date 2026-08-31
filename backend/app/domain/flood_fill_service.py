from collections import deque

from .board import Board
from .position import Position


class FloodFillService:

    def open(
        self,
        board: Board,
        start_position: Position,
        player_id: str,
    ) -> None:
        """
        セルを開く。

        adjacent_mines == 0 のセルは周囲も連鎖的に開く。
        """

        start = board.get_cell(start_position)

        # 既に開いている場合は何もしない
        if start.is_open:
            return

        # 自分のFlagが立っている場合は開けない
        if (
            start.is_flagged
            and start.flagged_by == player_id
        ):
            return

        queue = deque([start])

        while queue:

            cell = queue.popleft()

            if cell.is_open:
                continue

            # 自分のFlagが立っているセルは開かない
            if (
                cell.is_flagged
                and cell.flagged_by == player_id
            ):
                continue

            cell.open(player_id)

            # 数字があるセルなら連鎖終了
            if cell.adjacent_mines != 0:
                continue

            for neighbor in board.neighbors(cell.position):

                if neighbor.is_open:
                    continue

                if neighbor.is_mine:
                    continue

                # 自分のFlagがあるセルは連鎖対象にしない
                if (
                    neighbor.is_flagged
                    and neighbor.flagged_by == player_id
                ):
                    continue

                queue.append(neighbor)
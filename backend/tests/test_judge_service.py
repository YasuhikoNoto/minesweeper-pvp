from app.domain.board import Board
from app.domain.judge_service import JudgeService
from app.domain.position import Position


def create_judge_service() -> JudgeService:
    return JudgeService()


def test_is_clear_should_return_true_when_all_safe_cells_are_open():

    judge_service = create_judge_service()

    board = Board(
        width=3,
        height=3,
    )

    # (0, 0) を地雷にする
    board.get_cell(
        Position(0, 0),
    ).is_mine = True

    # 地雷以外のセルをすべて開く
    for row in board.cells:
        for cell in row:
            if not cell.is_mine:
                cell.is_open = True

    result = judge_service.is_clear(board)

    assert result is True


def test_is_clear_should_return_false_when_safe_cell_is_not_open():

    judge_service = create_judge_service()

    board = Board(
        width=3,
        height=3,
    )

    # (0, 0) を地雷にする
    board.get_cell(
        Position(0, 0),
    ).is_mine = True

    # 安全マスの一部だけ開く
    board.get_cell(
        Position(1, 0),
    ).is_open = True

    result = judge_service.is_clear(board)

    assert result is False


def test_is_clear_should_return_true_when_only_mines_are_unopened():

    judge_service = create_judge_service()

    board = Board(
        width=3,
        height=3,
    )

    # (0, 0) を地雷にする
    board.get_cell(
        Position(0, 0),
    ).is_mine = True

    # 安全マスをすべて開く
    for row in board.cells:
        for cell in row:
            if not cell.is_mine:
                cell.is_open = True

    # 地雷は未開封のまま
    assert board.get_cell(
        Position(0, 0),
    ).is_open is False

    result = judge_service.is_clear(board)

    assert result is True
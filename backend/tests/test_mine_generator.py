import pytest

from app.domain.board import Board
from app.domain.position import Position
from app.domain.mine_generator import MineGenerator


def test_generate_should_place_specified_number_of_mines(
    board: Board,
    mine_generator: MineGenerator,
):
    mine_generator.generate(
        board,
        mine_count=5,
        safe_position=Position(0, 0),
    )

    mine_count = sum(
        cell.is_mine
        for row in board.cells
        for cell in row
    )

    assert mine_count == 5


def test_generate_should_raise_error_when_mine_count_is_too_large(
    board: Board,
    mine_generator: MineGenerator,
):
    with pytest.raises(ValueError):
        mine_generator.generate(
            board,
            mine_count=25,
            safe_position=Position(0, 0),
        )


def test_generate_should_not_place_mine_on_safe_position(
    board: Board,
    mine_generator: MineGenerator,
):
    safe_position = Position(0, 0)

    mine_generator.generate(
        board,
        mine_count=5,
        safe_position=safe_position,
    )

    assert board.get_cell(
        safe_position,
    ).is_mine is False
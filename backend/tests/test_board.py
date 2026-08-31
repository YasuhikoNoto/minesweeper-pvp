import pytest

from app.domain.board import Board
from app.domain.position import Position


def test_get_cell_should_return_cell_at_position(board: Board):
    # Arrange
    position = Position(1, 2)

    # Act
    cell = board.get_cell(position)

    # Assert
    assert cell.position == position


def test_get_cell_should_raise_error_when_position_is_out_of_bounds(board: Board):
    # Act / Assert
    with pytest.raises(IndexError):
        board.get_cell(Position(-1, 0))


def test_in_bounds_should_return_true_for_valid_position(board: Board):
    assert board.in_bounds(Position(2, 2))


def test_in_bounds_should_return_false_for_invalid_position(board: Board):
    assert not board.in_bounds(Position(-1, 0))
    assert not board.in_bounds(Position(board.width, 0))
    assert not board.in_bounds(Position(0, board.height))


def test_neighbors_should_return_8_cells_for_center(board: Board):
    # Act
    neighbors = board.neighbors(Position(2, 2))

    # Assert
    assert len(neighbors) == 8


def test_neighbors_should_return_3_cells_for_corner(board: Board):
    neighbors = board.neighbors(Position(0, 0))

    assert len(neighbors) == 3


def test_neighbors_should_return_5_cells_for_edge(board: Board):
    neighbors = board.neighbors(Position(2, 0))

    assert len(neighbors) == 5
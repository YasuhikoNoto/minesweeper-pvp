import pytest

from app.domain.board import Board
from app.domain.flood_fill_service import FloodFillService
from app.domain.number_calculator import NumberCalculator
from app.domain.position import Position


def create_board_with_center_mine(
    number_calculator: NumberCalculator,
) -> Board:
    board = Board(3, 3)

    board.get_cell(Position(1, 1)).is_mine = True

    number_calculator.calculate(board)

    return board


def create_board_with_corner_mine(
    number_calculator: NumberCalculator,
) -> Board:
    board = Board(3, 3)

    board.get_cell(Position(2, 2)).is_mine = True

    number_calculator.calculate(board)

    return board


def test_open_should_open_selected_cell(
    flood_fill_service: FloodFillService,
    number_calculator: NumberCalculator,
):
    # Arrange
    board = create_board_with_center_mine(number_calculator)

    # Act
    flood_fill_service.open(
        board,
        Position(0, 0),
        "player-1",
    )

    # Assert
    assert board.get_cell(Position(0, 0)).is_open


def test_open_should_stop_at_numbered_cell(
    flood_fill_service: FloodFillService,
    number_calculator: NumberCalculator,
):
    # Arrange
    board = create_board_with_center_mine(number_calculator)

    # Act
    flood_fill_service.open(
        board,
        Position(0, 0),
        "player-1",
    )

    # Assert
    assert board.get_cell(Position(0, 0)).is_open
    assert not board.get_cell(Position(0, 1)).is_open


def test_open_should_expand_when_adjacent_mine_count_is_zero(
    flood_fill_service: FloodFillService,
    number_calculator: NumberCalculator,
):
    # Arrange
    board = create_board_with_corner_mine(number_calculator)

    # Act
    flood_fill_service.open(
        board,
        Position(0, 0),
        "player-1",
    )

    # Assert
    opened = sum(
        cell.is_open
        for row in board.cells
        for cell in row
    )

    assert opened > 1


def test_open_should_not_open_flagged_cell(
    flood_fill_service: FloodFillService,
    number_calculator: NumberCalculator,
):
    # Arrange
    board = create_board_with_corner_mine(number_calculator)

    cell = board.get_cell(Position(0, 0))
    cell.toggle_flag("player-1")

    # Act
    flood_fill_service.open(
        board,
        Position(0, 0),
        "player-1",
    )

    # Assert
    assert not cell.is_open


def test_open_should_not_open_mine_cell(
    flood_fill_service: FloodFillService,
    number_calculator: NumberCalculator,
):
    # Arrange
    board = create_board_with_corner_mine(number_calculator)

    # Act
    flood_fill_service.open(
        board,
        Position(0, 0),
        "player-1",
    )

    # Assert
    assert not board.get_cell(Position(2, 2)).is_open
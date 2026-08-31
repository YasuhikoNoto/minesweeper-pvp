import pytest

from app.domain.cell import Cell
from app.domain.exceptions import (
    CellAlreadyOpenedError,
    CellFlaggedError,
)
from app.domain.position import Position

def create_cell() -> Cell:
    return Cell(
        position=Position(0, 0),
    )


def test_open_should_open_cell():

    cell = create_cell()

    cell.open("player-1")

    assert cell.is_open is True


def test_open_should_raise_error_when_cell_is_already_open():

    cell = create_cell()

    cell.open("player-1")

    with pytest.raises(CellAlreadyOpenedError):
        cell.open("player-1")

    assert cell.is_open is True


def test_toggle_flag_should_flag_cell():

    cell = create_cell()

    cell.toggle_flag("player-1")

    assert cell.is_flagged is True


def test_toggle_flag_should_unflag_cell():

    cell = create_cell()

    cell.toggle_flag("player-1")
    cell.toggle_flag("player-1")

    assert cell.is_flagged is False
    assert cell.flagged_by is None


def test_toggle_flag_should_raise_error_when_cell_is_open():

    cell = Cell(
        position=Position(0, 0),
    )

    cell.is_open = True

    with pytest.raises(CellAlreadyOpenedError):
        cell.toggle_flag("player-1")

    assert cell.is_flagged is False


def test_open_should_record_player_id():
    cell = Cell(
        position=Position(0, 0),
    )

    cell.open("player-1")

    assert cell.is_open is True
    assert cell.opened_by == "player-1"


def test_opened_by_should_be_none_initially():
    cell = Cell(
        position=Position(0, 0),
    )

    assert cell.opened_by is None


def test_open_should_raise_error_when_cell_is_flagged_by_same_player():
    cell = Cell(
        position=Position(0, 0),
        flagged_by="player-1",
        is_flagged=True,
    )

    with pytest.raises(CellFlaggedError):
        cell.open("player-1")

    assert cell.is_open is False
    

def test_open_should_remove_opponent_flag_and_open_cell():
    cell = Cell(
        position=Position(0, 0),
        flagged_by="player-1",
        is_flagged=True,
    )

    cell.open("player-2")

    assert cell.is_open is True
    assert cell.opened_by == "player-2"
    assert cell.is_flagged is False
    assert cell.flagged_by is None


def test_toggle_flag_should_set_flagged_by():
    cell = Cell(
        position=Position(0, 0),
    )

    cell.toggle_flag("player-1")

    assert cell.flagged_by == "player-1"


def test_toggle_flag_should_remove_own_flag():
    cell = Cell(
        position=Position(0, 0),
        flagged_by="player-1",
    )

    cell.toggle_flag("player-1")

    assert cell.flagged_by is None
from unittest.mock import Mock

from app.domain.exceptions import CellFlaggedError
from app.domain.flood_fill_service import FloodFillService
from app.domain.game import Game
from app.domain.game_status import GameStatus
from app.domain.judge_service import JudgeService
from app.domain.mine_generator import MineGenerator
from app.domain.number_calculator import NumberCalculator
from app.domain.player import Player
from app.domain.position import Position
from app.services.game_service import GameService


def create_game() -> Game:
    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    game.add_player(
        Player(id="player-1"),
    )

    game.add_player(
        Player(id="player-2"),
    )

    return game


def create_game_service():
    mine_generator = Mock(spec=MineGenerator)
    number_calculator = Mock(spec=NumberCalculator)
    flood_fill_service = Mock(spec=FloodFillService)
    judge_service = Mock(spec=JudgeService)

    game_service = GameService(
        mine_generator=mine_generator,
        number_calculator=number_calculator,
        flood_fill_service=flood_fill_service,
        judge_service=judge_service,
    )

    return (
        game_service,
        mine_generator,
        number_calculator,
        flood_fill_service,
        judge_service,
    )


def test_start_should_only_start_game():

    (
        game_service,
        mine_generator,
        number_calculator,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game_service.start(game)

    mine_generator.generate.assert_not_called()
    number_calculator.calculate.assert_not_called()

    assert game.status == GameStatus.PLAYING


def test_open_should_open_cell():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        judge_service,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    judge_service.is_clear.return_value = False

    game_service.open(
        game,
        position,
        "player-1",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-1",
    )

    assert game.status == GameStatus.PLAYING


def test_open_should_change_status_to_game_over_when_opening_mine():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    mine_position = Position(1, 1)

    game.board.get_cell(
        mine_position,
    ).is_mine = True

    game_service.open(
        game,
        mine_position,
        "player-1",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        mine_position,
        "player-1",
    )

    assert game.status == GameStatus.GAME_OVER


def test_open_should_not_change_status_after_game_over():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.GAME_OVER

    game_service.open(
        game,
        Position(0, 0),
        "player-1",
    )

    flood_fill_service.open.assert_not_called()

    assert game.status == GameStatus.GAME_OVER


def test_open_should_not_change_status_after_clear():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.CLEAR

    game_service.open(
        game,
        Position(0, 0),
        "player-1",
    )

    flood_fill_service.open.assert_not_called()

    assert game.status == GameStatus.CLEAR


def test_open_should_raise_error_when_cell_is_flagged():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    cell = game.board.get_cell(position)
    cell.is_flagged = True
    cell.flagged_by = "player-1"

    try:
        game_service.open(
            game,
            position,
            "player-1",
        )
    except CellFlaggedError:
        pass
    else:
        raise AssertionError(
            "CellFlaggedErrorが発生しませんでした。"
        )

    flood_fill_service.open.assert_not_called()


def test_toggle_flag_should_toggle_flag():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    game_service.toggle_flag(
        game,
        position,
        "player-1",
    )

    cell = game.board.get_cell(position)

    assert cell.is_flagged is True
    assert cell.flagged_by == "player-1"


def test_open_should_raise_error_when_game_is_not_started():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.NOT_STARTED

    try:
        game_service.open(
            game,
            Position(0, 0),
            "player-1",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "ValueErrorが発生しませんでした。"
        )

    flood_fill_service.open.assert_not_called()


def test_toggle_flag_should_raise_error_when_game_is_not_started():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.NOT_STARTED

    try:
        game_service.toggle_flag(
            game,
            Position(0, 0),
            "player-1",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "ValueErrorが発生しませんでした。"
        )


def test_start_should_set_first_player_as_current_player():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game_service.start(game)

    assert game.current_player_id == "player-1"


def test_open_should_switch_turn():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        judge_service,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    judge_service.is_clear.return_value = False

    game_service.open(
        game,
        position,
        "player-1",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-1",
    )

    assert game.current_player_id == "player-2"


def test_open_should_raise_error_when_not_current_player():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    try:
        game_service.open(
            game,
            Position(0, 0),
            "player-2",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "ValueErrorが発生しませんでした。"
        )

    flood_fill_service.open.assert_not_called()

    assert game.current_player_id == "player-1"


def test_open_should_not_switch_turn_when_opening_mine():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    game.board.get_cell(
        position,
    ).is_mine = True

    game_service.open(
        game,
        position,
        "player-1",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-1",
    )

    assert game.status == GameStatus.GAME_OVER
    assert game.current_player_id == "player-1"


def test_toggle_flag_should_not_switch_turn():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    game_service.toggle_flag(
        game,
        Position(0, 0),
        "player-1",
    )

    assert game.current_player_id == "player-1"


def test_open_should_set_other_player_as_winner_when_opening_mine():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    game.board.get_cell(
        position,
    ).is_mine = True

    game_service.open(
        game,
        position,
        "player-1",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-1",
    )

    assert game.status == GameStatus.GAME_OVER
    assert game.winner_player_id == "player-2"


def test_open_should_set_other_player_as_winner_when_player_2_opens_mine():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-2"

    position = Position(0, 0)

    game.board.get_cell(
        position,
    ).is_mine = True

    game_service.open(
        game,
        position,
        "player-2",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-2",
    )

    assert game.status == GameStatus.GAME_OVER
    assert game.winner_player_id == "player-1"


def test_open_should_be_draw_when_all_safe_cells_are_open():

    (
        game_service,
        _,
        _,
        flood_fill_service,
        judge_service,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    judge_service.is_clear.return_value = True

    game_service.open(
        game,
        position,
        "player-1",
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-1",
    )

    assert game.status == GameStatus.CLEAR
    assert game.winner_player_id is None
    assert game.current_player_id == "player-1"


def test_toggle_flag_should_allow_current_player():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    game_service.toggle_flag(
        game,
        position,
        "player-1",
    )

    assert game.board.get_cell(
        position,
    ).is_flagged is True


def test_toggle_flag_should_raise_error_when_not_current_player():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    try:
        game_service.toggle_flag(
            game,
            position,
            "player-2",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "ValueErrorが発生しませんでした。"
        )

    assert game.board.get_cell(
        position,
    ).is_flagged is False


def test_toggle_flag_should_not_switch_turn_when_unflagging():

    (
        game_service,
        _,
        _,
        _,
        _,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    game_service.toggle_flag(
        game,
        position,
        "player-1",
    )

    assert game.board.get_cell(
        position,
    ).is_flagged is True

    game_service.toggle_flag(
        game,
        position,
        "player-1",
    )

    assert game.board.get_cell(
        position,
    ).is_flagged is False

    assert game.current_player_id == "player-1"


def test_open_should_generate_mines_on_first_open():

    (
        game_service,
        mine_generator,
        number_calculator,
        flood_fill_service,
        judge_service,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position = Position(0, 0)

    judge_service.is_clear.return_value = False

    game_service.open(
        game,
        position,
        "player-1",
    )

    mine_generator.generate.assert_called_once_with(
        game.board,
        game.mine_count,
        safe_position=position,
    )

    number_calculator.calculate.assert_called_once_with(
        game.board,
    )

    flood_fill_service.open.assert_called_once_with(
        game.board,
        position,
        "player-1",
    )


def test_open_should_not_generate_mines_after_first_open():

    (
        game_service,
        mine_generator,
        number_calculator,
        flood_fill_service,
        judge_service,
    ) = create_game_service()

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    position1 = Position(0, 0)
    position2 = Position(1, 1)

    judge_service.is_clear.return_value = False

    # 1回目のOpen
    game_service.open(
        game,
        position1,
        "player-1",
    )

    # 2回目のOpen
    game_service.open(
        game,
        position2,
        "player-2",
    )

    mine_generator.generate.assert_called_once_with(
        game.board,
        game.mine_count,
        safe_position=position1,
    )

    number_calculator.calculate.assert_called_once_with(
        game.board,
    )

    assert flood_fill_service.open.call_count == 2
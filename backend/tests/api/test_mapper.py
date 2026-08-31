from app.api.mapper import GameMapper
from app.domain.game import Game
from app.domain.game_status import GameStatus
from app.domain.player import Player
from app.domain.position import Position


def create_game() -> Game:
    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    game.add_player(Player(id="player-1"))
    game.add_player(Player(id="player-2"))

    return game


def test_to_response_should_return_winner_player_id():
    game = create_game()

    game.status = GameStatus.GAME_OVER
    game.winner_player_id = "player-2"

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    assert response.winner_player_id == "player-2"


def test_to_response_should_return_none_when_game_is_draw():
    game = create_game()

    game.status = GameStatus.CLEAR
    game.winner_player_id = None

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    assert response.winner_player_id is None


def test_to_response_should_show_cell_opened_by_self():
    game = create_game()

    cell = game.board.get_cell(
        Position(0, 0),
    )

    cell.is_open = True
    cell.opened_by = "player-1"
    cell.adjacent_mines = 2

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    response_cell = response.board.cells[0][0]

    assert response_cell.is_open is True
    assert response_cell.adjacent_mines == 2


def test_to_response_should_hide_cell_opened_by_opponent():
    game = create_game()

    cell = game.board.get_cell(
        Position(0, 0),
    )

    cell.is_open = True
    cell.opened_by = "player-2"
    cell.adjacent_mines = 2

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    response_cell = response.board.cells[0][0]

    assert response_cell.is_open is False
    assert response_cell.adjacent_mines is None


def test_to_response_should_show_flag_regardless_of_flag_owner():
    game = create_game()

    cell = game.board.get_cell(
        Position(0, 0),
    )

    cell.is_flagged = True
    cell.flagged_by = "player-2"

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    response_cell = response.board.cells[0][0]

    assert response_cell.is_flagged is True


def test_to_response_should_hide_adjacent_mines_when_cell_is_not_visible():
    game = create_game()

    cell = game.board.get_cell(
        Position(0, 0),
    )

    cell.is_open = False
    cell.adjacent_mines = 3

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    response_cell = response.board.cells[0][0]

    assert response_cell.is_open is False
    assert response_cell.adjacent_mines is None


def test_to_response_should_return_current_player_id():

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    assert response.current_player_id == "player-1"


def test_to_response_should_return_current_player_id_to_both_players():

    game = create_game()

    game.status = GameStatus.PLAYING
    game.current_player_id = "player-1"

    player1_response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-1",
    )

    player2_response = GameMapper.to_response(
        game_id="game-1",
        game=game,
        player_id="player-2",
    )

    assert player1_response.current_player_id == "player-1"
    assert player2_response.current_player_id == "player-1"
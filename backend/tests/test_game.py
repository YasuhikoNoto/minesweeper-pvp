import pytest

from app.domain.game import Game
from app.domain.game_status import GameStatus
from app.domain.player import Player


def create_game() -> Game:
    return Game(
        width=5,
        height=5,
        mine_count=3,
    )


def test_add_player():
    game = create_game()
    player = Player(id="player-1")

    game.add_player(player)

    assert game.players == [player]


def test_game_can_have_two_players():
    game = create_game()

    player1 = Player(id="player-1")
    player2 = Player(id="player-2")

    game.add_player(player1)
    game.add_player(player2)

    assert game.players == [
        player1,
        player2,
    ]


def test_add_player_should_raise_error_when_two_players_already_joined():
    game = create_game()

    game.add_player(Player(id="player-1"))
    game.add_player(Player(id="player-2"))

    with pytest.raises(ValueError):
        game.add_player(Player(id="player-3"))


def test_add_player_should_raise_error_when_same_player_already_joined():
    game = create_game()
    player = Player(id="player-1")

    game.add_player(player)

    with pytest.raises(ValueError):
        game.add_player(player)


def test_start_game_when_two_players_joined():

    game = create_game()

    game.add_player(Player(id="player-1"))
    game.add_player(Player(id="player-2"))

    game.start()

    assert game.status == GameStatus.PLAYING


def test_start_game_should_raise_error_when_no_players_joined():

    game = create_game()

    with pytest.raises(ValueError):
        game.start()

    assert game.status == GameStatus.NOT_STARTED


def test_start_game_should_raise_error_when_game_already_started():

    game = create_game()

    game.add_player(Player(id="player-1"))
    game.add_player(Player(id="player-2"))

    game.start()

    with pytest.raises(ValueError):
        game.start()

    assert game.status == GameStatus.PLAYING


def test_game_should_have_no_winner_when_created():

    game = create_game()

    assert game.winner_player_id is None


def test_start_game_should_set_first_player_as_current_player():

    game = create_game()

    game.add_player(Player(id="player-1"))
    game.add_player(Player(id="player-2"))

    game.start()

    assert game.current_player_id == "player-1"
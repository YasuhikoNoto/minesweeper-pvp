import pytest

from unittest.mock import Mock

from app.domain.game import Game
from app.domain.player import Player
from app.domain.position import Position
from app.repository.game_repository import GameRepository
from app.services.game_application_service import GameApplicationService
from app.services.game_service import GameService
from app.domain.game_status import GameStatus


def create_application_service():
    repository = Mock(spec=GameRepository)
    game_service = Mock(spec=GameService)

    application_service = GameApplicationService(
        repository=repository,
        game_service=game_service,
    )

    return application_service, repository, game_service


def test_create_game_should_save_game():

    application_service, repository, _ = create_application_service()

    repository.save.return_value = "game-id"

    result = application_service.create_game(
        width=5,
        height=5,
        mine_count=3,
        player_id="player-1",
    )

    assert result == "game-id"

    repository.save.assert_called_once()

    saved_game = repository.save.call_args.args[0]

    assert isinstance(saved_game, Game)
    assert saved_game.width == 5
    assert saved_game.height == 5
    assert saved_game.mine_count == 3


def test_find_game_should_return_game():

    application_service, repository, _ = create_application_service()

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    repository.find_by_id.return_value = game

    result = application_service.find_game("game-id")

    assert result is game

    repository.find_by_id.assert_called_once_with(
        "game-id",
    )


def test_join_game_should_add_player_and_update_game():

    application_service, repository, _ = create_application_service()

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    repository.find_by_id.return_value = game

    result = application_service.join_game(
        game_id="game-id",
        player_id="player-1",
    )

    repository.find_by_id.assert_called_once_with(
        "game-id",
    )

    repository.update.assert_called_once_with(
        "game-id",
        game,
    )

    assert result == Player(id="player-1")
    assert game.players == [
        Player(id="player-1"),
    ]


def test_start_game_should_start_and_update_game():

    application_service, repository, game_service = (
        create_application_service()
    )

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    repository.find_by_id.return_value = game

    result = application_service.start_game(
        game_id="game-id",
    )

    repository.find_by_id.assert_called_once_with(
        "game-id",
    )

    game_service.start.assert_called_once_with(
        game,
    )

    repository.update.assert_called_once_with(
        "game-id",
        game,
    )

    assert result is game


def test_open_cell_should_open_and_update_game():

    application_service, repository, game_service = (
        create_application_service()
    )

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    position = Position(1, 2)

    repository.find_by_id.return_value = game

    result = application_service.open_cell(
        "game-id",
        position,
        "player-1",
    )

    repository.find_by_id.assert_called_once_with(
        "game-id",
    )

    game_service.open.assert_called_once_with(
        game,
        position,
        "player-1",
    )

    repository.update.assert_called_once_with(
        "game-id",
        game,
    )

    assert result is game


def test_toggle_flag_should_toggle_and_update_game():

    application_service, repository, game_service = (
        create_application_service()
    )

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    position = Position(2, 3)

    repository.find_by_id.return_value = game

    result = application_service.toggle_flag(
        "game-id",
        position,
        "player-1",
    )

    repository.find_by_id.assert_called_once_with(
        "game-id",
    )

    game_service.toggle_flag.assert_called_once_with(
        game,
        position,
        "player-1",
    )

    repository.update.assert_called_once_with(
        "game-id",
        game,
    )

    assert result is game
    

def test_join_game_should_add_player_and_update_game():

    application_service, repository, _ = (
        create_application_service()
    )

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    repository.find_by_id.return_value = game

    result = application_service.join_game(
        "game-id",
        "player-1",
    )

    repository.find_by_id.assert_called_once_with(
        "game-id",
    )

    repository.update.assert_called_once_with(
        "game-id",
        game,
    )

    assert isinstance(result, Player)
    assert result.id == "player-1"

    assert len(game.players) == 1
    assert game.players[0] is result


def test_join_game_should_allow_two_players():

    application_service, repository, _ = (
        create_application_service()
    )

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    repository.find_by_id.return_value = game

    player1 = application_service.join_game(
        "game-id",
        "player-1",
    )

    player2 = application_service.join_game(
        "game-id",
        "player-2",
    )

    assert player1.id == "player-1"
    assert player2.id == "player-2"

    assert len(game.players) == 2
    assert game.players[0] is player1
    assert game.players[1] is player2


def test_join_game_should_raise_error_when_two_players_already_joined():

    application_service, repository, _ = (
        create_application_service()
    )

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    game.add_player(Player(id="player-1"))
    game.add_player(Player(id="player-2"))

    repository.find_by_id.return_value = game

    with pytest.raises(ValueError):
        application_service.join_game(
            "game-id",
            "player-3",
        )

    assert len(game.players) == 2

    repository.update.assert_not_called()


def test_rematch_game_should_create_new_game_from_game_over():

    application_service, repository, _ = (
        create_application_service()
    )

    old_game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    old_game.add_player(
        Player(id="player-1"),
    )
    old_game.add_player(
        Player(id="player-2"),
    )

    old_game.status = GameStatus.GAME_OVER

    repository.find_by_id.return_value = old_game
    repository.save.return_value = "new-game-id"

    result = application_service.rematch_game(
        game_id="old-game-id",
        player_id="player-1",
    )

    assert result == "new-game-id"

    repository.find_by_id.assert_called_once_with(
        "old-game-id",
    )

    repository.save.assert_called_once()

    new_game = repository.save.call_args.args[0]

    assert new_game is not old_game

    assert new_game.width == old_game.width
    assert new_game.height == old_game.height
    assert new_game.mine_count == old_game.mine_count

    assert new_game.players == [
        Player(id="player-1"),
        Player(id="player-2"),
    ]

    assert new_game.status == GameStatus.NOT_STARTED


def test_rematch_game_should_create_new_game_from_clear():

    application_service, repository, _ = (
        create_application_service()
    )

    old_game = Game(
        width=8,
        height=6,
        mine_count=10,
    )

    old_game.add_player(
        Player(id="player-1"),
    )
    old_game.add_player(
        Player(id="player-2"),
    )

    old_game.status = GameStatus.CLEAR

    repository.find_by_id.return_value = old_game
    repository.save.return_value = "new-game-id"

    result = application_service.rematch_game(
        game_id="old-game-id",
        player_id="player-2",
    )

    assert result == "new-game-id"

    new_game = repository.save.call_args.args[0]

    assert new_game is not old_game

    assert new_game.width == 8
    assert new_game.height == 6
    assert new_game.mine_count == 10

    assert new_game.players == [
        Player(id="player-1"),
        Player(id="player-2"),
    ]

    assert new_game.status == GameStatus.NOT_STARTED


@pytest.mark.parametrize(
    "status",
    [
        GameStatus.NOT_STARTED,
        GameStatus.PLAYING,
    ],
)
def test_rematch_game_should_raise_error_when_game_is_not_finished(
    status,
):

    application_service, repository, _ = (
        create_application_service()
    )

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

    game.status = status

    repository.find_by_id.return_value = game

    with pytest.raises(
        ValueError,
        match="終了したゲームのみ再戦できます。",
    ):
        application_service.rematch_game(
            game_id="game-id",
            player_id="player-1",
        )

    repository.save.assert_not_called()


def test_rematch_game_should_raise_error_for_non_player():

    application_service, repository, _ = (
        create_application_service()
    )

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

    game.status = GameStatus.GAME_OVER

    repository.find_by_id.return_value = game

    with pytest.raises(
        ValueError,
        match="このゲームのプレイヤーではありません。",
    ):
        application_service.rematch_game(
            game_id="game-id",
            player_id="player-3",
        )

    repository.save.assert_not_called()
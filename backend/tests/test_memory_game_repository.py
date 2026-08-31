import pytest

from app.domain.exceptions import GameNotFoundError
from app.domain.game import Game
from app.repository.memory_game_repository import MemoryGameRepository


def create_game() -> Game:
    return Game(
        width=5,
        height=5,
        mine_count=3,
    )


def test_save_should_return_game_id():

    repository = MemoryGameRepository()
    game = create_game()

    game_id = repository.save(game)

    assert game_id is not None
    assert isinstance(game_id, str)


def test_find_by_id_should_return_saved_game():

    repository = MemoryGameRepository()
    game = create_game()

    game_id = repository.save(game)

    result = repository.find_by_id(game_id)

    assert result is game


def test_update_should_replace_game():

    repository = MemoryGameRepository()

    game = create_game()
    game_id = repository.save(game)

    updated_game = Game(
        width=10,
        height=10,
        mine_count=10,
    )

    repository.update(
        game_id,
        updated_game,
    )

    result = repository.find_by_id(game_id)

    assert result is updated_game


def test_find_by_id_should_raise_error_when_game_does_not_exist():

    repository = MemoryGameRepository()

    with pytest.raises(GameNotFoundError):
        repository.find_by_id("unknown-game-id")
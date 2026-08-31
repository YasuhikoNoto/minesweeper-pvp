from app.domain.game import Game
from app.repository.game_repository import GameRepository


def test_save_should_return_game_id():
    repository = GameRepository()

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    game_id = repository.save(game)

    assert game_id


def test_find_by_id_should_return_saved_game():
    repository = GameRepository()

    game = Game(
        width=5,
        height=5,
        mine_count=3,
    )

    game_id = repository.save(game)

    saved = repository.find_by_id(game_id)

    assert saved is game
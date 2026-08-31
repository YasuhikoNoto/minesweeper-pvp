from app.domain.player import Player


def test_player_has_id():
    player = Player(id="player1")

    assert player.id == "player1"
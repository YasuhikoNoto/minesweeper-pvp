from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def create_started_game() -> str:
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["game_id"]

    response = client.post(
        f"/games/{game_id}/join",
        json={
            "player_id": "player-2",
        },
    )

    assert response.status_code == 200

    start_response = client.post(
        f"/games/{game_id}/start",
    )

    assert start_response.status_code == 200

    return game_id


def test_create_game():
    response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "game_id" in data
    assert isinstance(data["game_id"], str)


def test_find_game():
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["game_id"]

    response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-1",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["game_id"] == game_id
    assert data["width"] == 5
    assert data["height"] == 5
    assert data["mine_count"] == 3


def test_find_game_should_return_404_when_game_not_found():
    response = client.get(
        "/games/not-found-game-id",
        params={
            "player_id": "player-1",
        },
    )

    assert response.status_code == 404


def test_open_cell_should_return_422_when_position_is_negative():
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    game_id = create_response.json()["game_id"]

    response = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": -1,
            "y": 0,
        },
    )

    assert response.status_code == 422


def test_open_cell_should_return_400_when_position_is_out_of_bounds():
    game_id = create_started_game()

    response = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": 5,
            "y": 0,
        },
    )

    assert response.status_code == 400


def test_open_cell_should_return_400_when_cell_is_flagged():
    game_id = create_started_game()

    flag_response = client.post(
        f"/games/{game_id}/flag",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert flag_response.status_code == 200

    response = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert response.status_code == 400


def test_toggle_flag_should_return_400_when_cell_is_open():
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    game_id = create_response.json()["game_id"]

    # プレイヤー2参加
    response2 = client.post(
        f"/games/{game_id}/join",
        json={
            "player_id": "player-2",
        },
    )

    assert response2.status_code == 200

    # ゲーム開始
    start_response = client.post(
        f"/games/{game_id}/start",
    )

    assert start_response.status_code == 200

    # セルを開く
    open_response = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert open_response.status_code == 200

    # 開いたセルにフラグを立てようとする
    response = client.post(
        f"/games/{game_id}/flag",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert response.status_code == 400


def test_join_game():
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    game_id = create_response.json()["game_id"]

    response = client.post(
        f"/games/{game_id}/join",
        json={
            "player_id": "player-2",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["player_id"] == "player-2"


def test_start_game():
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    game_id = create_response.json()["game_id"]

    response2 = client.post(
        f"/games/{game_id}/join",
        json={
            "player_id": "player-2",
        },
    )

    assert response2.status_code == 200

    response = client.post(
        f"/games/{game_id}/start",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["game_id"] == game_id
    assert data["status"] == "PLAYING"


def test_find_game_should_return_board_from_player_perspective():
    # ゲーム作成
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["game_id"]

    # player-2参加
    response2 = client.post(
        f"/games/{game_id}/join",
        json={
            "player_id": "player-2",
        },
    )

    assert response2.status_code == 200

    # ゲーム開始
    start_response = client.post(
        f"/games/{game_id}/start",
    )

    assert start_response.status_code == 200

    # player-1が(0, 0)を開く
    open_response = client.post(
        f"/games/{game_id}/open",
        json={
            "x": 0,
            "y": 0,
            "player_id": "player-1",
        },
    )

    assert open_response.status_code == 200

    # player-1視点
    player1_response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-1",
        },
    )

    assert player1_response.status_code == 200

    # player-2視点
    player2_response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-2",
        },
    )

    assert player2_response.status_code == 200

    player1_board = player1_response.json()["board"]["cells"]
    player2_board = player2_response.json()["board"]["cells"]

    player1_cell = player1_board[0][0]
    player2_cell = player2_board[0][0]

    # player-1が開いたセルはplayer-1から見える
    assert player1_cell["is_open"] is True

    # player-2からは見えない
    assert player2_cell["is_open"] is False


def test_find_game_should_show_flag_to_both_players():
    # ゲーム作成
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["game_id"]

    # player-2参加
    response2 = client.post(
        f"/games/{game_id}/join",
        json={
            "player_id": "player-2",
        },
    )

    assert response2.status_code == 200

    # ゲーム開始
    start_response = client.post(
        f"/games/{game_id}/start",
    )

    assert start_response.status_code == 200

    # player-1が(0, 0)にFlagを立てる
    flag_response = client.post(
        f"/games/{game_id}/flag",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert flag_response.status_code == 200

    # player-1視点
    player1_response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-1",
        },
    )

    assert player1_response.status_code == 200

    # player-2視点
    player2_response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-2",
        },
    )

    assert player2_response.status_code == 200

    player1_board = player1_response.json()["board"]["cells"]
    player2_board = player2_response.json()["board"]["cells"]

    player1_cell = player1_board[0][0]
    player2_cell = player2_board[0][0]

    # Flagは両プレイヤーから見える
    assert player1_cell["is_flagged"] is True
    assert player2_cell["is_flagged"] is True


def test_open_cell_should_return_400_when_not_current_player():

    game_id = create_started_game()

    # player-1が先攻なので、player-1がセルを開く
    response1 = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert response1.status_code == 200

    # player-1が続けてセルを開こうとする
    # 現在はplayer-2のターンなので400になる
    response2 = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": 1,
            "y": 1,
        },
    )

    assert response2.status_code == 400


def test_find_game_should_show_only_cells_opened_by_current_player():
    # ゲーム作成
    create_response = client.post(
        "/games",
        json={
            "player_id": "player-1",
            "width": 5,
            "height": 5,
            "mine_count": 3,
        },
    )

    game_id = create_response.json()["game_id"]

    # 2人参加
    client.post(
        f"/games/{game_id}/join",
        json={"player_id": "player-1"},
    )

    client.post(
        f"/games/{game_id}/join",
        json={"player_id": "player-2"},
    )

    # 開始
    response = client.post(
        f"/games/{game_id}/start",
    )

    assert response.status_code == 200

    # player-1が(0, 0)を開く
    response = client.post(
        f"/games/{game_id}/open",
        json={
            "x": 0,
            "y": 0,
            "player_id": "player-1",
        },
    )

    assert response.status_code == 200

    # player-2が(4, 4)を開く
    response = client.post(
        f"/games/{game_id}/open",
        json={
            "x": 4,
            "y": 4,
            "player_id": "player-2",
        },
    )

    assert response.status_code == 200

    # player-1視点
    player1_response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-1",
        },
    )

    # player-2視点
    player2_response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-2",
        },
    )

    player1_cells = player1_response.json()["board"]["cells"]
    player2_cells = player2_response.json()["board"]["cells"]

    # player-1から見える
    assert player1_cells[0][0]["is_open"] is True

    # player-1からはplayer-2が開いたセルは見えない
    assert player1_cells[4][4]["is_open"] is False

    # player-2から見える
    assert player2_cells[4][4]["is_open"] is True

    # player-2からはplayer-1が開いたセルは見えない
    assert player2_cells[0][0]["is_open"] is False


def test_find_game_should_return_current_player_id():

    game_id = create_started_game()

    response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-1",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_player_id"] == "player-1"


def test_open_cell_should_switch_current_player_id():

    game_id = create_started_game()

    response = client.get(
        f"/games/{game_id}",
        params={
            "player_id": "player-1",
        },
    )

    assert response.json()["current_player_id"] == "player-1"

    response = client.post(
        f"/games/{game_id}/open",
        json={
            "player_id": "player-1",
            "x": 0,
            "y": 0,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_player_id"] == "player-2"
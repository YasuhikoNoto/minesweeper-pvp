from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.schemas import (
    CreateGameRequest,
    CreateGameResponse,
    OpenCellRequest,
    GameResponse,
    ToggleFlagRequest,
    JoinGameRequest,
    JoinGameResponse,
    RematchRequest,
    RematchResponse,
)

from app.api.mapper import GameMapper

from app.domain.position import Position

from app.domain.exceptions import (
    CellAlreadyOpenedError,
    CellFlaggedError,
)

from app.services.game_application_service import (
    GameApplicationService,
)

from app.dependencies import (
    get_game_application_service,
)

from app.websocket.connection_manager import (
    manager,
)


router = APIRouter()


@router.post(
    "/games",
    response_model=CreateGameResponse,
)
def create_game(
    request: CreateGameRequest,
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    game_id = application_service.create_game(
        width=request.width,
        height=request.height,
        mine_count=request.mine_count,
        player_id=request.player_id,
    )

    return CreateGameResponse(
        game_id=game_id,
    )


@router.post(
    "/games/{game_id}/join",
    response_model=JoinGameResponse,
)
async def join_game(
    game_id: str,
    request: JoinGameRequest,
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    try:
        player = application_service.join_game(
            game_id=game_id,
            player_id=request.player_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    await manager.broadcast(
        game_id,
        "PLAYER_JOINED",
    )

    return JoinGameResponse(
        player_id=player.id,
    )


@router.post(
    "/games/{game_id}/start",
    response_model=GameResponse,
)
async def start_game(
    game_id: str,
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    try:
        game = application_service.start_game(
            game_id=game_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    await manager.broadcast(
        game_id,
        "GAME_UPDATED",
    )

    # TODO:
    # start APIではまだ「誰の視点か」が決まっていない。
    # そのため、ここでプレイヤー視点のGameResponseを作るのは不自然。
    #
    # 今回は既存のテストを整理する段階で、
    # start APIのレスポンスモデルも後ほど見直す。

    return GameMapper.to_response(
        game_id,
        game,
        game.players[0].id,
    )

@router.post(
    "/games/{game_id}/rematch",
)
async def rematch_game(
    game_id: str,
    request: RematchRequest,
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    try:
        new_game_id = application_service.rematch_game(
            game_id,
            request.player_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    await manager.broadcast(
        game_id,
        f"REMATCH_CREATED:{new_game_id}",
    )

    return {
        "game_id": new_game_id,
    }

@router.post(
    "/games/{game_id}/open",
    response_model=GameResponse,
)
async def open_cell(
    game_id: str,
    request: OpenCellRequest,
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    try:
        game = application_service.open_cell(
            game_id,
            Position(
                request.x,
                request.y,
            ),
            request.player_id,
        )

    except IndexError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except CellFlaggedError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    await manager.broadcast(
        game_id,
        "CELL_OPENED",
    )

    return GameMapper.to_response(
        game_id,
        game,
        request.player_id,
    )


@router.post(
    "/games/{game_id}/flag",
    response_model=GameResponse,
)
async def toggle_flag(
    game_id: str,
    request: ToggleFlagRequest,
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    try:
        game = application_service.toggle_flag(
            game_id,
            Position(
                request.x,
                request.y,
            ),
            request.player_id,
        )

    except IndexError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except CellAlreadyOpenedError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    await manager.broadcast(
        game_id,
        "FLAG_TOGGLED",
    )

    return GameMapper.to_response(
        game_id,
        game,
        request.player_id,
    )


@router.get(
    "/games/{game_id}",
    response_model=GameResponse,
)
def find_game(
    game_id: str,
    player_id: str = Query(...),
    application_service: GameApplicationService = Depends(
        get_game_application_service,
    ),
):
    game = application_service.find_game(
        game_id,
    )

    return GameMapper.to_response(
        game_id,
        game,
        player_id,
    )
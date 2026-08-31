from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    player_id: str
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    mine_count: int = Field(gt=0)


class CreateGameResponse(BaseModel):
    game_id: str


class OpenCellRequest(BaseModel):
    player_id: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)


class OpenCellResponse(BaseModel):
    status: str


class CellResponse(BaseModel):
    x: int
    y: int
    is_open: bool
    is_opened_by_opponent: bool
    is_mine: bool
    is_flagged: bool
    adjacent_mines: int | None


class BoardResponse(BaseModel):
    width: int
    height: int
    cells: list[list[CellResponse]]


class GameResponse(BaseModel):
    game_id: str
    width: int
    height: int
    mine_count: int
    status: str
    current_player_id: str | None
    winner_player_id: str | None
    board: BoardResponse


class ToggleFlagRequest(BaseModel):
    player_id: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)


class JoinGameRequest(BaseModel):
    player_id: str


class JoinGameResponse(BaseModel):
    player_id: str


class RematchRequest(BaseModel):
    player_id: str


class RematchResponse(BaseModel):
    game_id: str
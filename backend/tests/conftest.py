import pytest

from app.domain.board import Board
from app.domain.flood_fill_service import FloodFillService
from app.domain.game import Game
from app.domain.judge_service import JudgeService
from app.domain.mine_generator import MineGenerator
from app.domain.number_calculator import NumberCalculator
from app.services.game_service import GameService
from app.repository.game_repository import GameRepository



@pytest.fixture
def board() -> Board:
    return Board(
        width=5,
        height=5,
    )


@pytest.fixture
def mine_generator() -> MineGenerator:
    return MineGenerator()


@pytest.fixture
def number_calculator() -> NumberCalculator:
    return NumberCalculator()


@pytest.fixture
def flood_fill_service() -> FloodFillService:
    return FloodFillService()


@pytest.fixture
def judge_service() -> JudgeService:
    return JudgeService()


@pytest.fixture
def game() -> Game:
    return Game(
        width=5,
        height=5,
        mine_count=3,
    )


@pytest.fixture
def game_service(
    mine_generator: MineGenerator,
    number_calculator: NumberCalculator,
    flood_fill_service: FloodFillService,
    judge_service: JudgeService,
) -> GameService:
    return GameService(
        mine_generator=mine_generator,
        number_calculator=number_calculator,
        flood_fill_service=flood_fill_service,
        judge_service=judge_service,
    )

@pytest.fixture
def game_repository() -> GameRepository:
    return GameRepository()
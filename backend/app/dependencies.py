from app.repository.game_repository import GameRepository

from app.domain.mine_generator import MineGenerator
from app.domain.number_calculator import NumberCalculator
from app.domain.flood_fill_service import FloodFillService
from app.domain.judge_service import JudgeService

from app.services.game_service import GameService
from app.services.game_application_service import GameApplicationService

_repository = GameRepository()


def get_game_repository() -> GameRepository:
    return _repository


def get_game_service() -> GameService:
    return GameService(
        mine_generator=MineGenerator(),
        number_calculator=NumberCalculator(),
        flood_fill_service=FloodFillService(),
        judge_service=JudgeService(),
    )


def get_game_application_service() -> GameApplicationService:
    return GameApplicationService(
        repository=get_game_repository(),
        game_service=get_game_service(),
    )
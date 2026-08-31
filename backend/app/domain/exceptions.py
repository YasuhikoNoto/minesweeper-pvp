class DomainError(Exception):
    """ドメイン例外の基底クラス"""


class CellFlaggedError(DomainError):
    """フラグ付きセルを開こうとした"""


class CellAlreadyOpenedError(DomainError):
    """開いているセルへフラグを立てようとした"""


class GameNotFoundError(DomainError):
    """ゲームが存在しない"""
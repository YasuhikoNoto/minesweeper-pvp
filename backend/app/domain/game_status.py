from enum import Enum


class GameStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    CLEAR = "CLEAR"
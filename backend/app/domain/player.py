from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    id: str
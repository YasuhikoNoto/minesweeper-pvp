from dataclasses import dataclass, field

from .cell import Cell
from .position import Position


@dataclass
class Board:
    width: int
    height: int

    cells: list[list[Cell]] = field(init=False)

    def __post_init__(self):
        self.cells = [
            [
                Cell(position=Position(x, y))
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def get_cell(self, position: Position) -> Cell:
        """
        指定座標のセルを取得する
        """

        if not self.in_bounds(position):
            raise IndexError(f"({position.x}, {position.y}) は盤面外です。")

        return self.cells[position.y][position.x]

    def in_bounds(self, position: Position) -> bool:
        """
        座標が盤面内か判定する
        """

        return (
            0 <= position.x < self.width
            and
            0 <= position.y < self.height
        )

    def neighbors(self, position: Position) -> list[Cell]:
        
        result = []
    
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
            
                if dx == 0 and dy == 0:
                    continue
    
                neighbor_position = Position(
                    x=position.x + dx,
                    y=position.y + dy,
                )
    
                if self.in_bounds(neighbor_position):
                    result.append(
                        self.get_cell(neighbor_position)
                    )
    
        return result
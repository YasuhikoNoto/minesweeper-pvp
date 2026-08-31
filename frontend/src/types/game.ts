export type GameStatus =
  | 'NOT_STARTED'
  | 'PLAYING'
  | 'GAME_OVER'
  | 'CLEAR'

export interface Position {
  x: number
  y: number
}

export interface Cell {
  position: Position
  isMine: boolean
  isOpen: boolean
  isOpenedByOpponent: boolean
  isFlagged: boolean
  adjacentMines: number | null
}

export interface Board {
  width: number
  height: number
  cells: Cell[][]
}

export interface Game {
  id: string
  width: number
  height: number
  mineCount: number
  status: GameStatus
  currentPlayerId: string | null
  winnerPlayerId: string | null
  board: Board
}
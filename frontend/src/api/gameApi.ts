import axios from 'axios'

import type {
  Board,
  Cell,
  Game,
  GameStatus,
} from '../types/game'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
})

// ==============================
// Request
// ==============================

export interface CreateGameRequest {
  player_id: string
  width: number
  height: number
  mine_count: number
}

export interface OpenCellRequest {
  player_id: string
  x: number
  y: number
}

export interface ToggleFlagRequest {
  player_id: string
  x: number
  y: number
}

export interface JoinGameRequest {
  player_id: string
}

export interface RematchRequest {
  player_id: string
}

// ==============================
// API Response
// ==============================

interface CreateGameApiResponse {
  game_id: string
}

interface CellApiResponse {
  x: number
  y: number
  is_open: boolean
  is_opened_by_opponent: boolean
  is_mine: boolean
  is_flagged: boolean
  adjacent_mines: number | null
}

interface BoardApiResponse {
  width: number
  height: number
  cells: CellApiResponse[][]
}

interface GameApiResponse {
  game_id: string
  width: number
  height: number
  mine_count: number
  status: GameStatus
  current_player_id: string | null
  winner_player_id: string | null
  board: BoardApiResponse
}

interface JoinGameApiResponse {
  player_id: string
}

interface RematchApiResponse {
  game_id: string
}

// ==============================
// Frontend Response
// ==============================

export interface CreateGameResponse {
  gameId: string
}

export interface OpenCellResponse {
  status: string
}

export interface RematchResponse {
  gameId: string
}

// ==============================
// Mapper
// ==============================

function toCell(
  cell: CellApiResponse,
): Cell {
  return {
    position: {
      x: cell.x,
      y: cell.y,
    },

    isMine: cell.is_mine,

    isOpen: cell.is_open,
    isOpenedByOpponent: cell.is_opened_by_opponent,
    isFlagged: cell.is_flagged,

    adjacentMines: cell.adjacent_mines ?? 0,
  }
}

function toBoard(
  board: BoardApiResponse,
): Board {
  return {
    width: board.width,
    height: board.height,

    cells: board.cells.map(
      row => row.map(toCell),
    ),
  }
}

function toGame(
  response: GameApiResponse,
): Game {
  return {
    id: response.game_id,

    width: response.width,
    height: response.height,

    mineCount: response.mine_count,

    status: response.status,

    currentPlayerId:
      response.current_player_id,

    winnerPlayerId:
      response.winner_player_id,

    board: toBoard(response.board),
  }
}

// ==============================
// API
// ==============================

export async function createGame(
  request: CreateGameRequest,
): Promise<CreateGameResponse> {

  const response =
    await apiClient.post<CreateGameApiResponse>(
      '/games',
      request,
    )

  return {
    gameId: response.data.game_id,
  }
}

export async function getGame(
  gameId: string,
  playerId: string,
): Promise<Game> {

  const response =
    await apiClient.get<GameApiResponse>(
      `/games/${gameId}`,
      {
        params: {
          player_id: playerId,
        },
      },
    )

  return toGame(response.data)
}

export async function openCell(
  gameId: string,
  request: OpenCellRequest,
): Promise<Game> {

  const response =
    await apiClient.post<GameApiResponse>(
      `/games/${gameId}/open`,
      request,
    )

  return toGame(response.data)
}

export async function toggleFlag(
  gameId: string,
  request: ToggleFlagRequest,
): Promise<Game> {

  const response =
    await apiClient.post<GameApiResponse>(
      `/games/${gameId}/flag`,
      request,
    )

  return toGame(response.data)
}

export async function joinGame(
  gameId: string,
  request: JoinGameRequest,
): Promise<string> {

  const response =
    await apiClient.post<JoinGameApiResponse>(
      `/games/${gameId}/join`,
      request,
    )

  return response.data.player_id
}

export async function startGame(
  gameId: string,
): Promise<Game> {

  const response =
    await apiClient.post<GameApiResponse>(
      `/games/${gameId}/start`,
    )

  return toGame(response.data)
}

export async function rematchGame(
  gameId: string,
  request: RematchRequest,
): Promise<RematchResponse> {

  const response =
    await apiClient.post<RematchApiResponse>(
      `/games/${gameId}/rematch`,
      request,
    )

  return {
    gameId: response.data.game_id,
  }
}
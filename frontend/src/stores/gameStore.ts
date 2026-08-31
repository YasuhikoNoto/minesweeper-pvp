import { ref } from 'vue'
import { defineStore } from 'pinia'

import {
  createGame as createGameApi,
  getGame,
  openCell as openCellApi,
  toggleFlag as toggleFlagApi,
  joinGame as joinGameApi,
  startGame as startGameApi,
  rematchGame as rematchGameApi,
} from '../api/gameApi'

import type {
  Game,
} from '../types/game'
import {
  connectGameWebSocket,
} from '../api/gameWebSocket'


export const useGameStore = defineStore('game', () => {
  const game = ref<Game | null>(null)
  const gameId = ref<string | null>(null)
  const playerId = ref<string | null>(null)

  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const socket = ref<WebSocket | null>(null)

  function setPlayerId(
    id: string,
  ): void {
    playerId.value = id

    localStorage.setItem(
      'playerId',
      id,
    )
  }

  async function createGame(
    width: number,
    height: number,
    mineCount: number,
  ): Promise<void> {
    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await createGameApi({
        player_id: playerId.value,
        width,
        height,
        mine_count: mineCount,
      })

      gameId.value = response.gameId

      localStorage.setItem(
        'gameId',
        response.gameId,
      )

      game.value = await getGame(
        response.gameId,
        playerId.value,
      )
    } catch (err) {
      error.value = 'ゲームの作成に失敗しました。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function loadGame(
    id: string,
  ): Promise<void> {
    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      game.value = await getGame(
        id,
        playerId.value,
      )

      gameId.value = id
    } catch (err) {
      error.value = 'ゲームの取得に失敗しました。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function openCell(
    x: number,
    y: number,
  ): Promise<Game> {
    if (gameId.value === null) {
      throw new Error('ゲームが選択されていません。')
    }

    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      game.value = await openCellApi(
        gameId.value,
        {
          player_id: playerId.value,
          x,
          y,
        },
      )

      return game.value

    } catch (err) {
      error.value = 'セルを開けませんでした。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function toggleFlag(
    x: number,
    y: number,
  ): Promise<void> {
    if (gameId.value === null) {
      throw new Error('ゲームが選択されていません。')
    }

    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      game.value = await toggleFlagApi(
        gameId.value,
        {
          player_id: playerId.value,
          x,
          y,
        },
      )
    } catch (err) {
      error.value = 'フラグの変更に失敗しました。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function joinGame(
    id: string,
  ): Promise<void> {
    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      await joinGameApi(
        id,
        {
          player_id: playerId.value,
        },
      )

      gameId.value = id

      localStorage.setItem(
        'gameId',
        id,
      )

      game.value = await getGame(
        id,
        playerId.value,
      )
    } catch (err) {
      error.value = 'ゲームへの参加に失敗しました。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function connectWebSocket(): void {
    if (gameId.value === null) {
      throw new Error('ゲームが選択されていません。')
    }
  
    if (socket.value !== null) {
      return
    }
  
    socket.value = connectGameWebSocket(
      gameId.value,
    )
  
    socket.value.onopen = () => {
      console.log('WebSocket connected')
    }
  
    socket.value.onmessage = async (event) => {
      if (
        gameId.value === null ||
        playerId.value === null
      ) {
        return
      }
    
      const message = event.data as string
    
      if (message.startsWith('REMATCH_CREATED:')) {
        const newGameId = message.replace(
          'REMATCH_CREATED:',
          '',
        )
      
        disconnectWebSocket()
      
        gameId.value = newGameId
      
        localStorage.setItem(
          'gameId',
          newGameId,
        )
      
        try {
          game.value = await getGame(
            newGameId,
            playerId.value,
          )
        
          connectWebSocket()
        } catch (err) {
          error.value = '再戦後のゲーム取得に失敗しました。'
        }
      
        return
      }
    
      game.value = await getGame(
        gameId.value,
        playerId.value,
      )
    }
  
    socket.value.onclose = () => {
      console.log('WebSocket disconnected')
      socket.value = null
    }
  
    socket.value.onerror = () => {
      console.error('WebSocket error')
    }
  }

  async function startGame(): Promise<void> {
    if (gameId.value === null) {
      throw new Error('ゲームが選択されていません。')
    }

    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      await startGameApi(
        gameId.value,
      )

      game.value = await getGame(
        gameId.value,
        playerId.value,
      )
    } catch (err) {
      error.value = 'ゲームの開始に失敗しました。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function rematchGame(): Promise<void> {
    if (gameId.value === null) {
      throw new Error('ゲームが選択されていません。')
    }

    if (playerId.value === null) {
      throw new Error('プレイヤーが設定されていません。')
    }

    isLoading.value = true
    error.value = null

    try {
      const oldGameId = gameId.value

      disconnectWebSocket()

      const response = await rematchGameApi(
        oldGameId,
        {
          player_id: playerId.value,
        },
      )

      gameId.value = response.gameId

      localStorage.setItem(
        'gameId',
        response.gameId,
      )

      game.value = await getGame(
        response.gameId,
        playerId.value,
      )

      connectWebSocket()

    } catch (err) {
      error.value = '再戦に失敗しました。'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function disconnectWebSocket(): void {
    if (socket.value === null) {
      return
    }

    socket.value.close()
    socket.value = null
  }

  function clearGame(): void {
    disconnectWebSocket()
  
    game.value = null
    gameId.value = null
  
    localStorage.removeItem('gameId')
  }

  return {
    game,
    gameId,
    playerId,
    isLoading,
    error,
    setPlayerId,
    createGame,
    loadGame,
    openCell,
    toggleFlag,
    joinGame,
    startGame,
    rematchGame,
    connectWebSocket,
    disconnectWebSocket,
    clearGame,
  }
})
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

import GameBoard from '../components/GameBoard.vue'
import { useGameStore } from '../stores/gameStore'

const gameStore = useGameStore()

const playerIdInput = ref('player-1')
const gameIdInput = ref('')

const width = ref(5)
const height = ref(5)
const mineCount = ref(3)

function setPlayerId(): void {
  gameStore.setPlayerId(
    playerIdInput.value,
  )
}

async function handleCreateGame(): Promise<void> {
  setPlayerId()

  await gameStore.createGame(
    width.value,
    height.value,
    mineCount.value,
  )

  gameStore.connectWebSocket()
}

async function handleJoinGame(): Promise<void> {
  setPlayerId()

  await gameStore.joinGame(
    gameIdInput.value,
  )

  gameStore.connectWebSocket()
}

async function handleStartGame(): Promise<void> {
  await gameStore.startGame()
}

const explosionPosition = ref<{
  x: number
  y: number
} | null>(null)

async function handleOpenCell(
  x: number,
  y: number,
): Promise<void> {
  const game = await gameStore.openCell(
    x,
    y,
  )

  const cell = game.board.cells[y][x]

  if (cell.isMine) {
    explosionPosition.value = {
      x,
      y,
    }
  }
}

async function handleToggleFlag(
  x: number,
  y: number,
): Promise<void> {
  await gameStore.toggleFlag(x, y)
}

async function handleRematchGame(): Promise<void> {
  await gameStore.rematchGame()
}

const isMyTurn = computed(() => {
  if (
    gameStore.game === null ||
    gameStore.playerId === null
  ) {
    return false
  }

  return (
    gameStore.game.currentPlayerId ===
    gameStore.playerId
  )
})

const turnMessage = computed(() => {
  if (gameStore.game === null) {
    return ''
  }

  if (isMyTurn.value) {
    return 'あなたのターンです'
  }

  return '相手のターンです'
})

const isGameFinished = computed(() => {
  if (gameStore.game === null) {
    return false
  }

  return (
    gameStore.game.status === 'GAME_OVER' ||
    gameStore.game.status === 'CLEAR'
  )
})

onMounted(async () => {
  const savedPlayerId =
    localStorage.getItem('playerId')

  const savedGameId =
    localStorage.getItem('gameId')

  if (
    savedPlayerId === null ||
    savedGameId === null
  ) {
    return
  }

  gameStore.setPlayerId(savedPlayerId)

  try {
    await gameStore.loadGame(
      savedGameId,
    )

    if (isGameFinished.value) {
      gameStore.clearGame()
      return
    }

    gameStore.connectWebSocket()
  } catch {
    gameStore.clearGame()
  }
})
</script>

<template>
  <main class="game-view">
    <header class="game-header">
      <h1>マインスイーパー PvP</h1>

      <p
        v-if="gameStore.error"
        class="error-message"
      >
        {{ gameStore.error }}
      </p>
    </header>

    <!-- ============================== -->
    <!-- ゲーム未選択 -->
    <!-- ============================== -->

    <template
      v-if="gameStore.game === null"
    >
      <section class="setup-panel">
        <h2>ゲームを開始</h2>

        <div class="setup-section">
          <h3>プレイヤー</h3>

          <label>
            プレイヤーID

            <input
              v-model="playerIdInput"
              type="text"
            />
          </label>
        </div>

        <div class="setup-section">
          <h3>ゲームを作成</h3>

          <div>
            <label>
              幅

              <input
                v-model.number="width"
                type="number"
                min="1"
              />
            </label>
          </div>

          <div>
            <label>
              高さ

              <input
                v-model.number="height"
                type="number"
                min="1"
              />
            </label>
          </div>

          <div>
            <label>
              地雷数

              <input
                v-model.number="mineCount"
                type="number"
                min="1"
              />
            </label>
          </div>

          <button
            :disabled="gameStore.isLoading"
            @click="handleCreateGame"
          >
            ゲームを作成
          </button>
        </div>

        <div class="setup-section">
          <h3>ゲームに参加</h3>

          <label>
            ゲームID

            <input
              v-model="gameIdInput"
              type="text"
            />
          </label>

          <button
            :disabled="gameStore.isLoading"
            @click="handleJoinGame"
          >
            ゲームに参加
          </button>
        </div>
      </section>
    </template>

    <!-- ============================== -->
    <!-- ゲーム選択済み -->
    <!-- ============================== -->

    <template v-else>
      <section class="game-info">
        <div>
          <span class="label">
            プレイヤー
          </span>

          <strong>
            {{ gameStore.playerId }}
          </strong>
        </div>

        <div>
          <span class="label">
            ゲームID
          </span>

          <strong>
            {{ gameStore.gameId }}
          </strong>
        </div>

        <div>
          <span class="label">
            状態
          </span>

          <strong>
            {{ gameStore.game.status }}
          </strong>
        </div>
      </section>

      <!-- ============================== -->
      <!-- 対戦準備中 -->
      <!-- ============================== -->

      <section
        v-if="
          gameStore.game.status ===
          'NOT_STARTED'
        "
        class="status-panel waiting"
      >
        <h2>対戦準備中</h2>

        <p>
          2人のプレイヤーが揃ったら
          ゲームを開始できます。
        </p>

        <button
          :disabled="gameStore.isLoading"
          @click="handleStartGame"
        >
          ゲーム開始
        </button>
      </section>

      <!-- ============================== -->
      <!-- ゲーム中 -->
      <!-- ============================== -->

      <section
        v-else-if="
          gameStore.game.status ===
          'PLAYING'
        "
        class="game-panel"
      >
        <div
          class="turn-panel"
          :class="{
            'my-turn': isMyTurn,
            'opponent-turn': !isMyTurn,
          }"
        >
          <span class="turn-label">
            TURN
          </span>

          <strong>
            {{ turnMessage }}
          </strong>
        </div>

        <div class="board-panel">
          <GameBoard
            :board="gameStore.game.board"
            :is-my-turn="isMyTurn"
            :explosion-position="explosionPosition"
            :is-game-finished="isGameFinished"
            @open="handleOpenCell"
            @toggle-flag="handleToggleFlag"
          />
        </div>

        <p class="game-hint">
          {{
            isMyTurn
              ? 'マスを開くか、右クリックでフラグを立てられます。'
              : '相手の操作を待っています。'
          }}
        </p>
      </section>

      <!-- ============================== -->
      <!-- GAME OVER -->
      <!-- ============================== -->

      <section
        v-else-if="
          gameStore.game.status ===
          'GAME_OVER'
        "
        class="result-panel game-over"
      >
        <h2>GAME OVER</h2>

        <p>
          Winner:
          <strong>
            {{ gameStore.game.winnerPlayerId }}
          </strong>
        </p>
      
        <GameBoard
          :board="gameStore.game.board"
          :is-my-turn="isMyTurn"
          :explosion-position="explosionPosition"
          :is-game-finished="isGameFinished"
          @open="handleOpenCell"
          @toggle-flag="handleToggleFlag"
        />
      
        <button
          :disabled="gameStore.isLoading"
          @click="handleRematchGame"
        >
          再戦
        </button>
      </section>

      <!-- ============================== -->
      <!-- CLEAR -->
      <!-- ============================== -->

      <section
        v-else-if="
          gameStore.game.status ===
          'CLEAR'
        "
        class="result-panel clear"
      >
        <h2>DRAW</h2>

        <p>
          全ての安全なセルが開かれました。
        </p>
      
        <GameBoard
          :board="gameStore.game.board"
          :is-my-turn="isMyTurn"
          :explosion-position="explosionPosition"
          :is-game-finished="isGameFinished"
          @open="handleOpenCell"
          @toggle-flag="handleToggleFlag"
        />
      
        <button
          :disabled="gameStore.isLoading"
          @click="handleRematchGame"
        >
          再戦
        </button>
      </section>
    </template>

    <p
      v-if="gameStore.isLoading"
      class="loading-message"
    >
      処理中...
    </p>
  </main>
</template>

<style scoped>
.game-view {
  width: min(900px, 100%);
  margin: 0 auto;
  padding: 32px 24px;
}

.game-header {
  margin-bottom: 24px;
}

.game-header h1 {
  margin: 0;
}

.error-message {
  margin-top: 12px;
}

.setup-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.setup-section {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.setup-section h3 {
  margin-top: 0;
}

.setup-section > div {
  margin-bottom: 12px;
}

.setup-section label {
  display: flex;
  gap: 8px;
  align-items: center;
}

.setup-section input {
  padding: 6px 8px;
}

.setup-section button {
  margin-top: 8px;
  padding: 8px 16px;
}

.game-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.game-info > div {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.label {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  opacity: 0.7;
}

.status-panel,
.result-panel {
  padding: 32px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 12px;
}

.status-panel h2,
.result-panel h2 {
  margin-top: 0;
}

.turn-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin-bottom: 24px;
  padding: 16px;
  border-radius: 10px;
}

.turn-panel.my-turn {
  border: 2px solid #333;
}

.turn-panel.opponent-turn {
  border: 1px solid #ccc;
  opacity: 0.75;
}

.turn-label {
  font-size: 12px;
  letter-spacing: 0.1em;
  opacity: 0.7;
}

.board-panel {
  display: flex;
  justify-content: center;
}

.game-hint {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  opacity: 0.7;
}

.result-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-message {
  margin-top: 20px;
  text-align: center;
}

.result-panel button {
  padding: 10px 24px;
}

@media (max-width: 600px) {
  .game-view {
    padding: 20px 12px;
  }

  .game-info {
    grid-template-columns: 1fr;
  }
}
</style>
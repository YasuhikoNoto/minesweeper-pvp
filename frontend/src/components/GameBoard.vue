<script setup lang="ts">
import Cell from './Cell.vue'
import type {
  Board,
  Cell as CellType,
} from '../types/game'

const props = defineProps<{
  board: Board
  isMyTurn: boolean
  explosionPosition: {
    x: number
    y: number
  } | null
  isGameFinished: boolean
}>()

const emit = defineEmits<{
  open: [x: number, y: number]
  toggleFlag: [x: number, y: number]
}>()

function handleOpen(
  cell: CellType,
): void {
  emit(
    'open',
    cell.position.x,
    cell.position.y,
  )
}

function handleToggleFlag(
  cell: CellType,
): void {
  emit(
    'toggleFlag',
    cell.position.x,
    cell.position.y,
  )
}
</script>

<template>
  <div
    class="game-board"
    :class="{
      'opponent-turn': !props.isMyTurn,
    }"
  >
    <div
      v-for="(row, y) in props.board.cells"
      :key="y"
      class="board-row"
    >
      <Cell
        v-for="(cell, x) in row"
        :key="x"
        :cell="cell"
        :disabled="!props.isMyTurn"
        :exploding="
          props.explosionPosition?.x === cell.position.x &&
          props.explosionPosition?.y === cell.position.y
        "
        :show-mine="
          props.isGameFinished &&
          cell.isMine
        "
        @open="handleOpen(cell)"
        @toggle-flag="handleToggleFlag(cell)"
      />
    </div>
  </div>
</template>

<style scoped>
.game-board {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.game-board.opponent-turn {
  opacity: 0.85;
}

.board-row {
  display: flex;
  gap: 2px;
}
</style>
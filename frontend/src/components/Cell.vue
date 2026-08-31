<script setup lang="ts">
import type { Cell } from '../types/game'

const props = defineProps<{
  cell: Cell
  disabled: boolean
  exploding: boolean
  showMine: boolean
}>()

const emit = defineEmits<{
  open: []
  toggleFlag: []
}>()

function handleClick(): void {
  if (
    props.disabled ||
    props.cell.isOpen ||
    props.cell.isOpenedByOpponent ||
    props.cell.isFlagged
  ) {
    return
  }

  emit('open')
}

function handleContextMenu(
  event: MouseEvent,
): void {
  event.preventDefault()

  if (
    props.disabled ||
    props.cell.isOpen ||
    props.cell.isOpenedByOpponent
  ) {
    return
  }

  emit('toggleFlag')
}
</script>

<template>
  <button
    class="cell"
    :class="{
      'is-disabled': props.disabled,
      'is-open': props.cell.isOpen,
      'is-opponent-opened':
        props.cell.isOpenedByOpponent,
      'is-flagged': props.cell.isFlagged,
      'is-exploding': props.exploding,
    }"
    :disabled="props.disabled"
    @click="handleClick"
    @contextmenu="handleContextMenu"
  >
    <template v-if="props.showMine">
      💣
    </template>

    <template v-else-if="cell.isOpen">
      {{ cell.adjacentMines }}
    </template>

    <template
      v-else-if="cell.isOpenedByOpponent"
    >
      ?
    </template>

    <template
      v-else-if="cell.isFlagged"
    >
      🚩
    </template>

    <template v-else>
      □
    </template>
  </button>
</template>

<style scoped>
.cell {
  width: 48px;
  height: 48px;
  padding: 0;

  font-size: 20px;
  font-weight: bold;

  border: 1px solid #999;
  border-radius: 4px;

  cursor: pointer;
}

.cell:not(:disabled):hover {
  transform: scale(1.05);
}

.cell.is-disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.cell.is-exploding {
  animation: explosion 0.6s ease-out;
}

@keyframes explosion {
  0% {
    transform: scale(1);
  }

  30% {
    transform: scale(1.4);
  }

  60% {
    transform: scale(0.85);
  }

  100% {
    transform: scale(1);
  }
}
</style>
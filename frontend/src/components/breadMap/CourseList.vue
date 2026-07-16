<script setup>
import { watch } from 'vue'

const props = defineProps({
  stops: { type: Array, required: true },
  selectedOrder: { type: Number, default: null },
})

const emit = defineEmits(['select'])

const itemRefs = new Map()

function setItemRef(order, el) {
  if (el) itemRefs.set(order, el)
  else itemRefs.delete(order)
}

// 지도 핀 클릭으로 선택이 바뀌면 해당 아이템이 보이도록 스크롤
watch(
  () => props.selectedOrder,
  (order) => {
    if (order == null) return
    itemRefs.get(order)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
  },
)

function kakaoLink(stop) {
  return `https://map.kakao.com/link/to/${encodeURIComponent(stop.name)},${stop.lat},${stop.lng}`
}

function toggleItem(order) {
  emit('select', props.selectedOrder === order ? null : order)
}
</script>

<template>
  <ol class="course-list">
    <li
      v-for="stop in stops"
      :key="stop.order"
      :ref="(el) => setItemRef(stop.order, el)"
      class="course-item"
      :class="{ 'course-item--selected': stop.order === selectedOrder }"
    >
      <button
        type="button"
        class="course-item__main"
        :aria-pressed="stop.order === selectedOrder"
        @click="toggleItem(stop.order)"
      >
        <span class="course-item__order">{{ stop.order }}</span>
        <span class="course-item__body">
          <span class="course-item__name">{{ stop.name }}</span>
          <span class="course-item__address">{{ stop.address }}</span>
          <span class="course-item__note">{{ stop.note }}</span>
        </span>
      </button>
      <a
        class="course-item__link"
        :href="kakaoLink(stop)"
        target="_blank"
        rel="noopener noreferrer"
        @click.stop
      >
        카카오맵 길찾기 ↗
      </a>
    </li>
  </ol>
</template>

<style scoped>
.course-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.course-item {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 4px solid transparent;
  border-radius: var(--radius-sm);
  transition: border-color 0.2s, background 0.2s;
}

.course-item:hover {
  border-color: var(--color-primary);
}

.course-item--selected {
  border-color: var(--color-accent);
  border-left-color: var(--color-accent);
  background: var(--color-primary-light);
}

.course-item__main {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px 8px;
  border: none;
  background: none;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
}

.course-item__main:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: -2px;
  border-radius: var(--radius-sm);
}

.course-item__order {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  font-size: var(--font-size-caption);
  font-weight: 700;
}

.course-item--selected .course-item__order {
  background: var(--color-accent);
}

.course-item__body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.course-item__name {
  font-size: var(--font-size-body);
  font-weight: 600;
  color: var(--color-text);
}

.course-item__address {
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.course-item__note {
  font-size: var(--font-size-caption);
  color: var(--color-text);
}

.course-item__link {
  align-self: flex-end;
  margin: 0 16px 12px;
  font-size: var(--font-size-caption);
  color: var(--color-accent-cyan);
  text-decoration: none;
}

.course-item__link:hover {
  color: var(--color-primary);
  text-decoration: underline;
}

.course-item__link:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-radius: 4px;
}
</style>

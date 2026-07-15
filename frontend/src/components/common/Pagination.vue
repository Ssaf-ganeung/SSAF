<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['update:currentPage'])

const pages = computed(() =>
  Array.from({ length: Math.max(props.totalPages, 0) }, (_, index) => index + 1)
)

function goTo(page) {
  if (page < 1 || page > props.totalPages || page === props.currentPage) return
  emit('update:currentPage', page)
}
</script>

<template>
  <nav class="pagination" aria-label="페이지 이동">
    <button
      type="button"
      class="pagination__arrow"
      :disabled="currentPage <= 1"
      @click="goTo(currentPage - 1)"
    >
      &lt;
    </button>

    <button
      v-for="page in pages"
      :key="page"
      type="button"
      class="pagination__page"
      :class="{ 'pagination__page--active': page === currentPage }"
      @click="goTo(page)"
    >
      {{ page }}
    </button>

    <button
      type="button"
      class="pagination__arrow"
      :disabled="currentPage >= totalPages"
      @click="goTo(currentPage + 1)"
    >
      &gt;
    </button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.pagination__arrow,
.pagination__page {
  min-width: 32px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  background: none;
  color: var(--color-text);
  font-size: var(--font-size-small);
  cursor: pointer;
}

.pagination__arrow:disabled {
  color: var(--color-text-secondary);
  cursor: not-allowed;
  opacity: 0.5;
}

.pagination__page:hover {
  color: var(--color-primary);
}

.pagination__page--active {
  border-color: var(--color-primary);
  color: var(--color-primary);
  font-weight: 600;
}
</style>

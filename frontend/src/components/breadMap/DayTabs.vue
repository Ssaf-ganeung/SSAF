<script setup>
defineProps({
  modelValue: { type: Number, required: true },
  days: { type: Array, required: true },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="day-tabs" role="tablist" aria-label="코스 선택">
    <button
      v-for="d in days"
      :key="d.day"
      type="button"
      role="tab"
      class="day-tab"
      :class="{ 'day-tab--active': d.day === modelValue }"
      :aria-selected="d.day === modelValue"
      @click="emit('update:modelValue', d.day)"
    >
      <span class="day-tab__icon" aria-hidden="true">
        {{ d.mode === 'walking' ? '🚶' : '🚗' }}
      </span>
      <span class="day-tab__day">Day {{ d.day }}</span>
      <span class="day-tab__title">{{ d.title }}</span>
    </button>
  </div>
</template>

<style scoped>
.day-tabs {
  display: flex;
  gap: 12px;
}

.day-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 14px 16px;
  font-family: inherit;
  font-size: var(--font-size-body);
  color: var(--color-text);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}

.day-tab:hover {
  border-color: var(--color-primary);
}

.day-tab:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.day-tab--active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

.day-tab__day {
  font-weight: 700;
}

.day-tab__title {
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
}

.day-tab--active .day-tab__title {
  color: rgba(255, 255, 255, 0.85);
}

@media (max-width: 820px) {
  .day-tabs {
    flex-direction: column;
  }

  .day-tab {
    justify-content: flex-start;
  }
}
</style>

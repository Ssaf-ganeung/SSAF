<script setup>
import { PLACE_TYPES } from "../../constants/placeTypes";

defineProps({
  modelValue: { type: String, required: true },
  disabled: { type: Boolean, default: false },
});

const emit = defineEmits(["update:modelValue"]);
</script>

<template>
  <div class="category-tabs" role="tablist" aria-label="카테고리 선택">
    <button
      v-for="placeType in PLACE_TYPES"
      :key="placeType.id"
      type="button"
      role="tab"
      class="category-tab"
      :class="{ 'category-tab--active': placeType.id === modelValue }"
      :aria-selected="placeType.id === modelValue"
      :disabled="disabled"
      @click="emit('update:modelValue', placeType.id)"
    >
      {{ placeType.name }}
    </button>
  </div>
</template>

<style scoped>
.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-tab {
  padding: 10px 18px;
  font-family: inherit;
  font-size: var(--font-size-body);
  color: var(--color-text);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}

.category-tab:hover {
  border-color: var(--color-primary);
}

.category-tab:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.category-tab:disabled {
  cursor: default;
  opacity: 0.6;
}

.category-tab--active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
  font-weight: 700;
}
</style>

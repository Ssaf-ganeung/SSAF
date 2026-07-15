<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger-outline'].includes(value),
  },
})
</script>

<template>
  <button type="button" class="base-button" :class="`base-button--${variant}`">
    <slot />
  </button>
</template>

<style scoped>
.base-button {
  height: 44px;
  padding: 0 20px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: var(--font-size-body);
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s, border-color 0.15s, color 0.15s;
}

.base-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.base-button--primary {
  border: 1px solid var(--color-primary);
  background: var(--color-primary);
  color: var(--color-surface);
}

.base-button--primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

.base-button--secondary {
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
}

.base-button--secondary:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.base-button--danger-outline {
  border: 1px solid var(--color-danger);
  background: var(--color-surface);
  color: var(--color-danger);
}

.base-button--danger-outline:hover:not(:disabled) {
  background: var(--color-danger);
  color: var(--color-surface);
}
</style>

<script setup>
defineProps({
  items: { type: Array, required: true },
})
</script>

<template>
  <nav class="breadcrumb" aria-label="breadcrumb">
    <template v-for="(item, index) in items" :key="item.label">
      <RouterLink v-if="item.to" :to="item.to" class="breadcrumb__link">{{ item.label }}</RouterLink>
      <span v-else class="breadcrumb__current">{{ item.label }}</span>
      <span v-if="index < items.length - 1" class="breadcrumb__separator">&gt;</span>
    </template>
  </nav>
</template>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.breadcrumb__link {
  color: var(--color-text-secondary);
  text-decoration: none;
}

.breadcrumb__link:hover {
  color: var(--color-primary);
}

.breadcrumb__current {
  color: var(--color-text-secondary);
}

.breadcrumb__separator {
  color: var(--color-text-secondary);
}
</style>

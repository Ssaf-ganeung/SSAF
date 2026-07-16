<script setup>
import { formatDate } from '../../utils/date'

defineProps({
  post: { type: Object, required: true },
  number: { type: Number, required: true },
})
</script>

<template>
  <tr class="post-row">
    <td class="post-row__number">{{ number }}</td>
    <td class="post-row__title">
      <RouterLink :to="`/community/${post.id}`" class="post-row__link">{{ post.title }}</RouterLink>
    </td>
    <td class="post-row__date">{{ formatDate(post.created_at) }}</td>
  </tr>
</template>

<style scoped>
.post-row {
  border-bottom: 1px solid var(--color-border);
}

.post-row td {
  height: 52px;
  padding: 0 12px;
}

.post-row__number {
  width: 80px;
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}

.post-row__title {
  text-align: left;
}

.post-row__link {
  color: var(--color-text);
  font-size: var(--font-size-body);
  text-decoration: none;
}

.post-row__link:hover {
  color: var(--color-primary);
}

.post-row__date {
  width: 120px;
  text-align: right;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
</style>

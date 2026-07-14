<script setup>
defineProps({
  post: { type: Object, required: true },
})
</script>

<template>
  <article>
    <RouterLink :to="`/community/${post.id}`">{{ post.title }}</RouterLink>
  </article>
</template>

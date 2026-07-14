<script setup>
defineProps({
  role: { type: String, required: true }, // 'user' | 'assistant'
  content: { type: String, required: true },
})
</script>

<template>
  <p :class="['chat-message', role]">{{ content }}</p>
</template>

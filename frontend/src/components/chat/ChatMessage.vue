<script setup>
defineProps({
  role: { type: String, required: true }, // 'user' | 'assistant'
  content: { type: String, required: true },
})
</script>

<template>
  <div :class="['chat-message', role]">{{ content }}</div>
</template>

<style scoped>
.chat-message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap; /* 줄바꿈 유지 */
  word-break: break-word;
}

/* 사용자 말풍선: 오른쪽, 헤더(#408a5c)에 흰색을 섞은 연한 초록 */
.chat-message.user {
  align-self: flex-end;
  background: #8cb99d;
  color: #1a1a1a;
  border-bottom-right-radius: 2px;
}

/* 봇 말풍선: 왼쪽, 흰색 */
.chat-message.assistant {
  align-self: flex-start;
  background: #fff;
  color: #222;
  border: 1px solid #e3e6ea;
  border-bottom-left-radius: 2px;
}
</style>

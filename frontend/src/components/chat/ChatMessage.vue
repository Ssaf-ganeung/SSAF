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

/* 사용자 말풍선: 오른쪽, 파란색 */
.chat-message.user {
  align-self: flex-end;
  background: #2f6fed;
  color: #fff;
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

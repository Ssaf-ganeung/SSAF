<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false }, // 로딩 중이면 입력 잠금
})
const emit = defineEmits(['send'])
const text = ref('')

function submit() {
  if (props.disabled) return
  if (!text.value.trim()) return
  emit('send', text.value)
  text.value = ''
}
</script>

<template>
  <form class="chat-input" @submit.prevent="submit">
    <input
      v-model="text"
      type="text"
      :disabled="disabled"
      placeholder="궁금한 지역 정보를 물어보세요"
    />
    <button type="submit" :disabled="disabled || !text.trim()">전송</button>
  </form>
</template>

<style scoped>
.chat-input {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid #e3e6ea;
  background: #fff;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d0d5db;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
}

.chat-input input:disabled {
  background: #f0f1f3;
}

.chat-input button {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background: #2f6fed;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.chat-input button:disabled {
  background: #a9c0f5;
  cursor: not-allowed;
}
</style>

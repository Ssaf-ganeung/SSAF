<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send'])
const text = ref('')

function submit() {
  if (!text.value.trim()) return
  emit('send', text.value)
  text.value = ''
}
</script>

<template>
  <form class="chat-input" @submit.prevent="submit">
    <input v-model="text" type="text" placeholder="궁금한 지역 정보를 물어보세요" />
    <button type="submit">전송</button>
  </form>
</template>

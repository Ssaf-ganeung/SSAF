<script setup>
import { useChatStore } from '../../stores/chat'
import ChatWindow from './ChatWindow.vue'
import ChatInput from './ChatInput.vue'
import { sendChatMessage } from '../../api/chat'

const chatStore = useChatStore()

async function handleSend(text) {
  chatStore.addMessage('user', text)
  // TODO: 백엔드 /api/chat 구현 후 실제 응답으로 교체
  const response = await sendChatMessage(text)
  chatStore.addMessage('assistant', response.data?.reply ?? '')
}
</script>

<template>
  <div class="chat-widget">
    <button class="chat-widget__toggle" @click="chatStore.toggle">💬</button>
    <div v-if="chatStore.isOpen" class="chat-widget__panel">
      <ChatWindow />
      <ChatInput @send="handleSend" />
    </div>
  </div>
</template>

<script setup>
import { useChatStore } from '../../stores/chat'
import ChatWindow from './ChatWindow.vue'
import ChatInput from './ChatInput.vue'
import { sendChatMessage } from '../../api/chat'

const chatStore = useChatStore()

async function handleSend(text) {
  chatStore.addMessage('user', text)
  // 방금 추가한 사용자 메시지를 포함한 대화 전체를 전송(맥락 유지)
  const response = await sendChatMessage(chatStore.messages)
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

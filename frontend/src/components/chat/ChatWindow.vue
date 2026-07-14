<script setup>
import { useChatStore } from '../../stores/chat'
import ChatMessage from './ChatMessage.vue'

const chatStore = useChatStore()
</script>

<template>
  <div class="chat-window">
    <ChatMessage
      v-for="(message, index) in chatStore.messages"
      :key="index"
      :role="message.role"
      :content="message.content"
    />
  </div>
</template>

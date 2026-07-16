<script setup>
import { useChatStore } from '../../stores/chat'
import ChatWindow from './ChatWindow.vue'
import ChatInput from './ChatInput.vue'
import { sendChatMessage } from '../../api/chat'
import mascot from '../../assets/chatbot-mascot.png'

const chatStore = useChatStore()

async function handleSend(text) {
  chatStore.addMessage('user', text)
  chatStore.setLoading(true)
  try {
    // 방금 추가한 사용자 메시지를 포함한 대화 전체를 전송(맥락 유지)
    const response = await sendChatMessage(chatStore.messages)
    chatStore.addMessage('assistant', response.data?.reply ?? '')
  } catch (err) {
    // 네트워크 오류/서버 다운 등 → 대화창에 안내 표시
    console.error('[chat] 전송 실패:', err)
    chatStore.addMessage('assistant', '⚠️ 답변을 가져오지 못했어요. 잠시 후 다시 시도해 주세요.')
  } finally {
    chatStore.setLoading(false)
  }
}
</script>

<template>
  <div class="chat-widget">
    <!-- 접힌 상태: 우하단 플로팅 버튼 -->
    <button
      v-if="!chatStore.isOpen"
      class="chat-widget__toggle"
      aria-label="챗봇 열기"
      @click="chatStore.toggle"
    >
      <img :src="mascot" alt="챗봇" class="chat-widget__mascot" />
    </button>

    <!-- 펼친 상태: 대화 패널 -->
    <div v-else class="chat-widget__panel">
      <header class="chat-widget__header">
        <span>대·충 봇</span>
        <button class="chat-widget__close" aria-label="챗봇 닫기" @click="chatStore.toggle">
          ✕
        </button>
      </header>
      <ChatWindow />
      <ChatInput :disabled="chatStore.isLoading" @send="handleSend" />
    </div>
  </div>
</template>

<style scoped>
.chat-widget__toggle {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 144px;
  height: 144px;
  padding: 0;
  border: none;
  border-radius: 50%;
  /* 흰 배경에서도 튀도록 진한 원형 배경 + 청록 그림자 */
  background: rgba(64, 138, 92, 0.53);

  cursor: pointer;
  z-index: 1000;
  box-shadow: 0 8px 22px rgba(0, 67, 70, 0.28); 
  transition: transform 0.15s, box-shadow 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}
.chat-widget__toggle:hover {
  transform: scale(1.06);
  box-shadow: 0 10px 28px rgba(41, 90, 60, 0.42);
}
.chat-widget__mascot {
  /* 로봇이 원 안에 들어오도록 원 크기에 맞춤 */
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  filter: drop-shadow(0 3px 5px rgba(0, 0, 0, 0.18));
}

.chat-widget__panel {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 360px;
  height: 520px;
  max-height: calc(100vh - 48px);
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  z-index: 1000;
}

.chat-widget__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #2f6fed;
  color: #fff;
  font-weight: 600;
}

.chat-widget__close {
  border: none;
  background: transparent;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

/* 모바일: 전체 화면으로 */
@media (max-width: 480px) {
  .chat-widget__panel {
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }
}
</style>

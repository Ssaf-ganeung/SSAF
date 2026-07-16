<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatStore } from '../../stores/chat'
import ChatMessage from './ChatMessage.vue'
import FloatingFaces from './FloatingFaces.vue'

const chatStore = useChatStore();
const scrollRef = ref(null);

// 새 메시지가 쌓이거나 로딩 상태가 바뀌면 맨 아래로 스크롤
async function scrollToBottom() {
  await nextTick(); // DOM 갱신 후에 스크롤해야 정확함
  const el = scrollRef.value;
  if (el) el.scrollTop = el.scrollHeight;
}

watch(() => [chatStore.messages.length, chatStore.isLoading], scrollToBottom);
</script>

<template>
  <div ref="scrollRef" class="chat-window">
    <FloatingFaces />

    <!-- 대화가 없을 때 안내 -->
    <p v-if="chatStore.messages.length === 0" class="chat-window__empty">
      안녕하세요!<br />
      대전·충청권 지역 정보를 물어보세요. 🗺️
    </p>

    <ChatMessage
      v-for="(message, index) in chatStore.messages"
      :key="index"
      :role="message.role"
      :content="message.content"
      :related-places="message.relatedPlaces ?? []"
      :related-posts="message.relatedPosts ?? []"
    />

    <!-- 답변 대기 중 표시 -->
    <p v-if="chatStore.isLoading" class="chat-window__typing">
      대·충 봇이 입력 중…
    </p>
  </div>
</template>

<style scoped>
.chat-window {
  position: relative; /* 떠다니는 팀원 사진의 배치 기준 */
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #f7f8fa;
}

/* 대화 내용은 항상 배경 사진 위에 */
.chat-window__empty,
.chat-window__typing {
  position: relative;
  z-index: 1;
}

.chat-window__empty {
  margin: auto;
  color: #313030;
  text-align: center;
  font-size: 14px;
}

.chat-window__typing {
  align-self: flex-start;
  color: #888;
  font-size: 13px;
  font-style: italic;
}
</style>

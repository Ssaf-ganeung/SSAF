<script setup>
import { onBeforeUnmount, ref } from 'vue'
import { useChatStore } from '../../stores/chat'
import ChatWindow from './ChatWindow.vue'
import ChatInput from './ChatInput.vue'
import { sendChatMessage } from '../../api/chat'
import mascot from '../../assets/chatbot-mascot.png'
import peekRobot from '../../assets/chatbot-peek.png'

const chatStore = useChatStore()

// 패널 크기. ChatWidget은 열고 닫아도 언마운트되지 않으므로 조절한 크기가 유지된다.
const MIN_W = 300
const MIN_H = 380
const MAX_W = 560
const panelW = ref(360)
const panelH = ref(520)

let startX = 0
let startY = 0
let startW = 0
let startH = 0

function clamp(value, lo, hi) {
  return Math.min(hi, Math.max(lo, value))
}

function onResizeStart(event) {
  startX = event.clientX
  startY = event.clientY
  startW = panelW.value
  startH = panelH.value
  window.addEventListener('pointermove', onResizeMove)
  window.addEventListener('pointerup', onResizeEnd)
  event.preventDefault() // 드래그 중 텍스트 선택 방지
}

function onResizeMove(event) {
  // 패널이 우하단에 고정이라, 좌상단 손잡이를 왼쪽·위로 끌수록 커진다.
  panelW.value = clamp(startW + (startX - event.clientX), MIN_W, MAX_W)
  panelH.value = clamp(startH + (startY - event.clientY), MIN_H, window.innerHeight - 48)
}

function onResizeEnd() {
  window.removeEventListener('pointermove', onResizeMove)
  window.removeEventListener('pointerup', onResizeEnd)
}

onBeforeUnmount(onResizeEnd)

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
    <div v-else class="chat-widget__dock">
      <!-- 패널 뒤에서 위로 삐져나와, 벽에 걸친 것처럼 가슴까지만 보인다 -->
      <img :src="peekRobot" alt="" class="chat-widget__robot" aria-hidden="true" />

      <div
        class="chat-widget__panel"
        :style="{ '--panel-w': panelW + 'px', '--panel-h': panelH + 'px' }"
      >
        <span
          class="chat-widget__resize"
          aria-hidden="true"
          @pointerdown="onResizeStart"
        ></span>

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

.chat-widget__dock {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 1000;
}

.chat-widget__panel {
  position: relative;
  z-index: 1; /* 로봇의 아랫부분을 가려 '벽에 걸친' 모양을 만든다 */
  width: var(--panel-w);
  height: var(--panel-h);
  max-height: calc(100vh - 48px);
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

/* 로봇: 패널 뒤(z-index 0)에 두고 아래쪽 일부를 패널에 걸쳐 가린다 */
.chat-widget__robot {
  position: absolute;
  z-index: 0;
  left: 50%;
  /* 이미지 높이의 약 25%가 패널에 가려져 가슴선에서 잘린다 (130px * 0.25) */
  bottom: calc(100% - 32px);
  width: 141px; /* 원본 304x280 비율 유지 -> 높이 약 130px */
  transform: translateX(-50%);
  pointer-events: none;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.18));
}

/* 좌상단 크기 조절 손잡이 (패널이 우하단 고정이라 반대편 모서리를 잡는다) */
.chat-widget__resize {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 2;
  width: 20px;
  height: 20px;
  cursor: nwse-resize;
  touch-action: none;
}

.chat-widget__resize::after {
  content: '';
  position: absolute;
  top: 5px;
  left: 5px;
  width: 7px;
  height: 7px;
  border-top: 2px solid rgba(255, 255, 255, 0.7);
  border-left: 2px solid rgba(255, 255, 255, 0.7);
  border-radius: 1px;
}

.chat-widget__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  /* 토글 버튼 원과 같은 계열의 초록 (흰 글씨 대비 확보를 위해 불투명하게) */
  background: #408a5c;
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

/* 모바일: 전체 화면으로. 크기 조절과 로봇은 공간이 없어 뺀다. */
@media (max-width: 480px) {
  .chat-widget__dock {
    right: 0;
    bottom: 0;
  }

  .chat-widget__panel {
    width: 100vw;
    /* dvh는 주소창을 뺀 실제 보이는 높이. vh만 쓰면 입력창이 화면 밖으로 밀린다. */
    height: 100vh;
    height: 100dvh;
    max-height: 100dvh;
    border-radius: 0;
  }

  /* 화면을 덮는 챗봇 버튼은 부담스러우므로 줄인다 */
  .chat-widget__toggle {
    right: 16px;
    bottom: 16px;
    width: 88px;
    height: 88px;
  }

  .chat-widget__robot,
  .chat-widget__resize {
    display: none;
  }
}
</style>

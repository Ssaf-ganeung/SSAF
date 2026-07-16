<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import hyoeun from '../../assets/face-hyoeun.png'
import subin from '../../assets/face-subin.png'
import minjun from '../../assets/face-minjun.png'

const faces = [hyoeun, subin, minjun]
const SWAP_INTERVAL = 10000 // 10초마다 교체

const index = ref(Math.floor(Math.random() * faces.length))
let timer = null

// 직전과 같은 사람이 또 뽑히면 바뀐 티가 안 나므로, 자기 자신은 빼고 고른다
function pickNext() {
  const offset = 1 + Math.floor(Math.random() * (faces.length - 1))
  index.value = (index.value + offset) % faces.length
}

onMounted(() => {
  timer = setInterval(pickNext, SWAP_INTERVAL)
})

onUnmounted(() => {
  clearInterval(timer) // 위젯을 닫아도 타이머가 남지 않도록
})
</script>

<template>
  <div class="floating-faces" aria-hidden="true">
    <Transition name="face-fade" mode="out-in">
      <img :key="index" :src="faces[index]" alt="" class="floating-faces__item" />
    </Transition>
  </div>
</template>

<style scoped>
.floating-faces {
  position: absolute;
  inset: 0;
  overflow: hidden; /* 떠다니다 채팅창 밖으로 삐져나가지 않도록 */
  pointer-events: none;
  z-index: 0; /* 대화 말풍선(z-index: 1)보다 뒤 */
}

/* 채팅창 하단 중앙 = 입력창 바로 위 */
.floating-faces__item {
  position: absolute;
  bottom: 8px;
  left: 50%;
  margin-left: -54px; /* width의 절반. 중앙 정렬을 transform으로 하면 애니메이션과 충돌한다 */
  width: 108px;
  height: auto;
  opacity: 0.9;
  animation: face-bob 4s ease-in-out infinite;
}

/* 위아래로만 천천히 */
@keyframes face-bob {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-12px);
  }
}

/* 교체될 때 툭 끊기지 않게 부드럽게 */
.face-fade-enter-active,
.face-fade-leave-active {
  transition: opacity 0.6s ease;
}

.face-fade-enter-from,
.face-fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .floating-faces__item {
    animation: none;
  }
}
</style>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import walkA from '../../assets/mascot-walk-1.png'
import walkB from '../../assets/mascot-walk-2.png'
import frontImg from '../../assets/mascot-front.png'

// 한쪽 끝에서 반대쪽 끝까지 걷는 시간. CSS의 transition 시간과 반드시 같아야 한다.
const WALK_MS = 8750
// 양 끝에 도착해서 정면을 보고 쉬는 시간
const PAUSE_MS = 1600
// 걷기 두 프레임을 번갈아 보여주는 주기. 이동 속도와 함께 조절해야 발이 미끄러지지 않는다.
const FRAME_MS = 288

const walking = ref(false)
const atRight = ref(false) // 현재 향하는(또는 머무는) 지점이 오른쪽 끝인지
const stepFrame = ref(0)

let timer = null
let frameTimer = null

// 원본 이미지가 오른쪽을 보고 있으므로, 왼쪽으로 갈 때만 뒤집는다.
const flipped = computed(() => walking.value && !atRight.value)

const src = computed(() => {
  if (!walking.value) return frontImg
  return stepFrame.value === 0 ? walkA : walkB
})

function startWalk() {
  walking.value = true
  atRight.value = !atRight.value // left 값이 바뀌며 CSS transition으로 이동
  frameTimer = setInterval(() => {
    stepFrame.value = stepFrame.value === 0 ? 1 : 0
  }, FRAME_MS)
  timer = setTimeout(arrive, WALK_MS)
}

function arrive() {
  walking.value = false
  clearInterval(frameTimer)
  timer = setTimeout(startWalk, PAUSE_MS)
}

onMounted(() => {
  // 애니메이션을 원치 않는 사용자에게는 왼쪽 끝에 가만히 서 있게 둔다.
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) return
  timer = setTimeout(startWalk, PAUSE_MS)
})

onBeforeUnmount(() => {
  clearTimeout(timer)
  clearInterval(frameTimer)
})
</script>

<template>
  <div class="mascot-walker" aria-hidden="true">
    <div
      class="mascot-walker__char"
      :class="{
        'mascot-walker__char--right': atRight,
        'mascot-walker__char--flip': flipped,
        'mascot-walker__char--walking': walking,
      }"
    >
      <img :src="src" alt="" class="mascot-walker__img" />
    </div>
  </div>
</template>

<style scoped>
.mascot-walker {
  position: absolute;
  inset: 0;
  overflow: hidden; /* 끝에서 헤더 밖으로 삐져나가지 않도록 */
  pointer-events: none;
  z-index: 0; /* 로고·네비게이션(z-index: 1)보다 뒤 */
}

.mascot-walker__char {
  position: absolute;
  bottom: 0;
  left: 0;
  transition: left 8750ms linear; /* WALK_MS와 동일 */
}

.mascot-walker__char--right {
  left: calc(100% - 34px); /* 캐릭터 폭만큼 빼서 오른쪽 끝에 맞춤 */
}

.mascot-walker__char--flip {
  transform: scaleX(-1);
}

/* 걷는 동안만 살짝 통통 튀게 (만화 느낌) */
.mascot-walker__char--walking .mascot-walker__img {
  animation: mascot-bob 576ms ease-in-out infinite; /* FRAME_MS x 2 */
}

.mascot-walker__img {
  display: block;
  height: 44px;
  width: auto;
}

@keyframes mascot-bob {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

/* 모바일에서는 공간이 좁아 로고와 겹치기만 하므로 숨긴다 */
@media (max-width: 640px) {
  .mascot-walker {
    display: none;
  }
}
</style>

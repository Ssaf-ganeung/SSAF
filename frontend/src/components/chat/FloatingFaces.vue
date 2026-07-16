<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import hyoeun from '../../assets/face-hyoeun.png'
import subin from '../../assets/face-subin.png'
import minjun from '../../assets/face-minjun.png'

const faces = [hyoeun, subin, minjun]
const SWAP_INTERVAL = 10000 // 10초마다 교체

// 프레임당 이동 픽셀. 채팅 배경이라 눈에 거슬리지 않게 느리게 둔다.
const MIN_SPEED = 0.25
const MAX_SPEED = 0.7
const SIZE = 108 // .floating-faces__mover 의 크기와 같아야 벽 계산이 맞는다

const index = ref(Math.floor(Math.random() * faces.length))
const rootRef = ref(null)
const moverRef = ref(null)

let timer = null
let rafId = null
let observer = null

// 위치와 속도. 반응형으로 두면 매 프레임 렌더가 돌아 무거워지므로 평범한 객체로 둔다.
const body = { x: 0, y: 0, vx: 0, vy: 0 }

// 직전과 같은 사람이 또 뽑히면 바뀐 티가 안 나므로, 자기 자신은 빼고 고른다
function pickNext() {
  const offset = 1 + Math.floor(Math.random() * (faces.length - 1))
  index.value = (index.value + offset) % faces.length
}

function randomSpeed() {
  const speed = MIN_SPEED + Math.random() * (MAX_SPEED - MIN_SPEED)
  return Math.random() < 0.5 ? -speed : speed
}

function bounds() {
  const el = rootRef.value
  if (!el) return { maxX: 0, maxY: 0 }
  return {
    maxX: Math.max(el.clientWidth - SIZE, 0),
    maxY: Math.max(el.clientHeight - SIZE, 0),
  }
}

function start() {
  const { maxX, maxY } = bounds()
  body.x = Math.random() * maxX
  body.y = Math.random() * maxY
  body.vx = randomSpeed()
  body.vy = randomSpeed()
}

function draw() {
  if (moverRef.value) {
    moverRef.value.style.transform = `translate(${body.x.toFixed(2)}px, ${body.y.toFixed(2)}px)`
  }
}

function tick() {
  const { maxX, maxY } = bounds()

  body.x += body.vx
  body.y += body.vy

  // 벽에 닿으면 방향을 뒤집는다. 위치도 벽 안으로 되돌려야 벽에 붙어 떠는 걸 막는다.
  if (body.x <= 0) {
    body.x = 0
    body.vx = Math.abs(body.vx)
  } else if (body.x >= maxX) {
    body.x = maxX
    body.vx = -Math.abs(body.vx)
  }

  if (body.y <= 0) {
    body.y = 0
    body.vy = Math.abs(body.vy)
  } else if (body.y >= maxY) {
    body.y = maxY
    body.vy = -Math.abs(body.vy)
  }

  draw()
  rafId = requestAnimationFrame(tick)
}

function clampIntoBounds() {
  // 챗봇 패널은 크기 조절이 되므로 줄이면 얼굴이 밖에 남을 수 있다.
  const { maxX, maxY } = bounds()
  body.x = Math.min(body.x, maxX)
  body.y = Math.min(body.y, maxY)
  draw()
}

onMounted(() => {
  start()
  timer = setInterval(pickNext, SWAP_INTERVAL)

  // 움직임을 원치 않는 사용자에게는 제자리에 두고 굴리지 않는다.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    draw()
    return
  }

  // 창 리사이즈만으로는 패널 크기 조절을 못 잡는다.
  if (rootRef.value && 'ResizeObserver' in window) {
    observer = new ResizeObserver(clampIntoBounds)
    observer.observe(rootRef.value)
  }
  rafId = requestAnimationFrame(tick)
})

onUnmounted(() => {
  clearInterval(timer) // 위젯을 닫아도 타이머가 남지 않도록
  if (rafId) cancelAnimationFrame(rafId)
  observer?.disconnect()
})
</script>

<template>
  <div ref="rootRef" class="floating-faces" aria-hidden="true">
    <!-- 이동은 이 상자가 담당하고, 교체는 안쪽 이미지만 한다 (서로 간섭하지 않도록) -->
    <div ref="moverRef" class="floating-faces__mover">
      <Transition name="face-fade" mode="out-in">
        <img :key="index" :src="faces[index]" alt="" class="floating-faces__item" />
      </Transition>
    </div>
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

.floating-faces__mover {
  position: absolute;
  top: 0;
  left: 0; /* 실제 위치는 JS가 transform으로 잡는다 */
  width: 108px; /* SIZE 상수와 같아야 한다 */
  height: 108px;
  will-change: transform;
}

.floating-faces__item {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 사진마다 비율이 달라도 상자 안에 맞춘다 */
  opacity: 0.9;
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
</style>

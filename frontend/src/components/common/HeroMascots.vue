<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ggumdori from '../../assets/Daejeon_mascots/ggumdori.png'
import first from '../../assets/Daejeon_mascots/first.png'
import second from '../../assets/Daejeon_mascots/second.png'
import third from '../../assets/Daejeon_mascots/third.png'
import maknaeng from '../../assets/Daejeon_mascots/maknaeng.png'
import ganadi from '../../assets/Daejeon_mascots/ganadi.png'
import nev from '../../assets/Daejeon_mascots/nev.png'

const mascots = [
  { src: ggumdori, name: '꿈돌이' },
  { src: first, name: '첫째' },
  { src: second, name: '둘째' },
  { src: third, name: '셋째' },
  { src: maknaeng, name: '막냉이' },
  { src: ganadi, name: '가나디' },
  { src: nev, name: '네브' },
]

// 커서를 따라가는 정도. 7명 모두 같은 값이라 대형을 유지한 채 함께 움직인다.
const FOLLOW = 0.2
const EASING = 0.08 // 목표 지점까지 매 프레임 좁히는 비율. 낮을수록 느긋하게 따라온다.

const rootRef = ref(null)
const itemEls = []
// 울타리 = 부모인 .hero. 이 안에서만 돌아다닌다.
let fenceEl = null
// 각 마스코트의 기준 위치(울타리 기준 상대 좌표). transform이 0일 때의 자리.
let bases = []
// 지금 적용 중인 이동량. 목표값으로 매 프레임 조금씩 다가간다.
let current = mascots.map(() => ({ x: 0, y: 0 }))
let cursor = { x: 0, y: 0 }
let following = false
let rafId = null

function setItemRef(el, index) {
  if (el) itemEls[index] = el
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max)
}

/** 기준 위치를 다시 잰다. transform을 잠시 걷어내야 원래 자리를 알 수 있다. */
function measure() {
  if (!fenceEl) return
  itemEls.forEach((el) => {
    if (el) el.style.transform = 'translate(0, 0)'
  })
  const fence = fenceEl.getBoundingClientRect()
  bases = itemEls.map((el) => {
    const r = el.getBoundingClientRect()
    return {
      left: r.left - fence.left, // 스크롤에 흔들리지 않도록 울타리 기준 상대 좌표로
      top: r.top - fence.top,
      width: r.width,
      height: r.height,
    }
  })
  current = mascots.map(() => ({ x: 0, y: 0 }))
}

function onMouseMove(event) {
  cursor = { x: event.clientX, y: event.clientY }
  following = true
}

function tick() {
  if (fenceEl && bases.length) {
    // 매 프레임 재서 스크롤·리사이즈에도 경계가 맞게 한다.
    const fence = fenceEl.getBoundingClientRect()
    const cursorX = cursor.x - fence.left
    const cursorY = cursor.y - fence.top

    mascots.forEach((mascot, i) => {
      const base = bases[i]
      const el = itemEls[i]
      if (!base || !el) return

      let targetX = 0
      let targetY = 0
      if (following) {
        targetX = (cursorX - (base.left + base.width / 2)) * FOLLOW
        targetY = (cursorY - (base.top + base.height / 2)) * FOLLOW
      }

      // 울타리 밖으로는 못 나간다
      targetX = clamp(targetX, -base.left, fence.width - (base.left + base.width))
      targetY = clamp(targetY, -base.top, fence.height - (base.top + base.height))

      current[i].x += (targetX - current[i].x) * EASING
      current[i].y += (targetY - current[i].y) * EASING
      el.style.transform = `translate(${current[i].x.toFixed(2)}px, ${current[i].y.toFixed(2)}px)`
    })
  }
  rafId = requestAnimationFrame(tick)
}

onMounted(() => {
  // 울타리는 부모(.hero). 없으면 자기 자신으로 물러선다.
  fenceEl = rootRef.value?.parentElement ?? rootRef.value
  measure()
  // 움직임을 원치 않는 사용자에게는 따라다니지 않는다
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  // 커서가 페이지 어디에 있든 반응하도록 window에 건다(움직임은 울타리 안으로 제한)
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('resize', measure)
  rafId = requestAnimationFrame(tick)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('resize', measure)
  if (rafId) cancelAnimationFrame(rafId)
})
</script>

<template>
  <div ref="rootRef" class="hero-mascots">
    <img
      v-for="(mascot, index) in mascots"
      :key="mascot.name"
      :ref="(el) => setItemRef(el, index)"
      :src="mascot.src"
      :alt="mascot.name"
      class="hero-mascots__item"
      @load="measure"
    />
  </div>
</template>

<style scoped>
.hero-mascots {
  position: relative;
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
  /* 울타리는 부모(.hero)이므로 여기서 자르지 않는다 */
}

.hero-mascots__item {
  width: 83px;
  height: auto;
  flex-shrink: 0;
  will-change: transform;
  user-select: none;
  -webkit-user-drag: none;
}

@media (max-width: 768px) {
  .hero-mascots {
    gap: 8px;
  }
  .hero-mascots__item {
    width: 57px;
  }
}
</style>

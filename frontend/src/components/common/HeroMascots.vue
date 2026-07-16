<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ggumdori from '../../assets/Daejeon_mascots/ggumdori.png'
import first from '../../assets/Daejeon_mascots/first.png'
import second from '../../assets/Daejeon_mascots/second.png'
import third from '../../assets/Daejeon_mascots/third.png'
import maknaeng from '../../assets/Daejeon_mascots/maknaeng.png'
import ganadi from '../../assets/Daejeon_mascots/ganadi.png'
import nev from '../../assets/Daejeon_mascots/nev.png'

// ease: 목표 지점까지 매 프레임 좁히는 비율 = 따라오는 속도.
// 꿈돌이가 가장 커서 제일 먼저 출발하고, 뒤로 갈수록 느려져 뒤따라 모여든다.
const mascots = [
  { src: ggumdori, name: '꿈돌이', ease: 0.101 },
  { src: first, name: '첫째', ease: 0.05 },
  { src: second, name: '둘째', ease: 0.04 },
  { src: third, name: '셋째', ease: 0.031 },
  { src: maknaeng, name: '막냉이', ease: 0.023 },
  { src: ganadi, name: '가나디', ease: 0.017 },
  { src: nev, name: '네브', ease: 0.013 },
]

// 커서 쪽으로 얼마나 모여드는지. 1이면 커서 자리까지 그대로 간다.
const FOLLOW = 1

// 서로 겹쳐도 되는 한도. 중심 사이 거리를 (두 폭의 평균 × 0.8) 이상으로 유지 → 최대 20% 겹침.
const OVERLAP = 0.9

const rootRef = ref(null)
const itemEls = []
// 울타리 = 부모인 .hero. 이 안에서만 돌아다닌다.
let fenceEl = null
// 각 마스코트의 기준 위치(울타리 기준 상대 좌표). transform이 0일 때의 자리.
let bases = []
// 지금 있는 자리(울타리 기준 중심 좌표). 각자 따로 움직이므로 대형은 유지되지 않는다.
let pos = mascots.map(() => ({ cx: 0, cy: 0 }))
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
  pos = bases.map((b) => ({ cx: b.left + b.width / 2, cy: b.top + b.height / 2 }))
}

/** 너무 가까운 둘을 서로 반대로 밀어 겹침이 20%를 넘지 않게 한다. */
function separate() {
  for (let i = 0; i < pos.length; i++) {
    for (let j = i + 1; j < pos.length; j++) {
      const a = bases[i]
      const b = bases[j]
      if (!a || !b) continue

      let dx = pos[j].cx - pos[i].cx
      let dy = pos[j].cy - pos[i].cy
      let dist = Math.hypot(dx, dy)
      const minDist = ((a.width + b.width) / 2) * OVERLAP
      if (dist >= minDist) continue

      // 완전히 포개지면 방향을 못 정하므로 아무 쪽으로나 떼어놓는다
      if (dist < 0.01) {
        dx = 1
        dy = 0
        dist = 1
      }
      const push = (minDist - dist) / 2
      const nx = (dx / dist) * push
      const ny = (dy / dist) * push
      pos[i].cx -= nx
      pos[i].cy -= ny
      pos[j].cx += nx
      pos[j].cy += ny
    }
  }
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

    // 1) 각자 자기 속도로 커서를 향해 간다. 커서가 없으면 제자리로 돌아간다.
    mascots.forEach((mascot, i) => {
      const base = bases[i]
      if (!base) return
      const homeCx = base.left + base.width / 2
      const homeCy = base.top + base.height / 2
      const targetCx = following ? homeCx + (cursorX - homeCx) * FOLLOW : homeCx
      const targetCy = following ? homeCy + (cursorY - homeCy) * FOLLOW : homeCy
      pos[i].cx += (targetCx - pos[i].cx) * mascot.ease
      pos[i].cy += (targetCy - pos[i].cy) * mascot.ease
    })

    // 2) 한 점으로 모이면 다 포개지므로, 20%까지만 겹치게 서로 밀어낸다
    separate()

    // 3) 울타리 안으로 가둔 뒤 그린다
    mascots.forEach((mascot, i) => {
      const base = bases[i]
      const el = itemEls[i]
      if (!base || !el) return
      const halfW = base.width / 2
      const halfH = base.height / 2
      pos[i].cx = clamp(pos[i].cx, halfW, fence.width - halfW)
      pos[i].cy = clamp(pos[i].cy, halfH, fence.height - halfH)
      const dx = pos[i].cx - (base.left + halfW)
      const dy = pos[i].cy - (base.top + halfH)
      el.style.transform = `translate(${dx.toFixed(2)}px, ${dy.toFixed(2)}px)`
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
      :style="{ zIndex: mascots.length - index }"
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

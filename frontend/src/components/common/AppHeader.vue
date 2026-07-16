<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import MascotWalker from './MascotWalker.vue'

// 데스크톱 가로 메뉴와 모바일 사이드바가 같은 목록을 쓰도록 한곳에 모아둔다
const navLinks = [
  { to: '/community', label: '게시판' },
  { to: '/map', label: '지도' },
  { to: '/bread-map', label: '빵지순례' },
  { to: '/local-info', label: '지역 정보' },
]

const isMenuOpen = ref(false)
const route = useRoute()

function closeMenu() {
  isMenuOpen.value = false
}

// 메뉴에서 링크를 누르면 페이지만 바뀌고 사이드바가 남아 있으면 안 된다
watch(() => route.fullPath, closeMenu)

// 사이드바가 열린 동안 뒤 페이지가 스크롤되지 않도록
watch(isMenuOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

function onKeydown(event) {
  if (event.key === 'Escape') closeMenu()
}

// 데스크톱 폭으로 넓히면 가로 메뉴가 돌아오므로 사이드바는 닫는다. CSS 미디어쿼리와 같은 값.
const desktopMq = window.matchMedia('(min-width: 769px)')

function onBreakpointChange(event) {
  if (event.matches) closeMenu()
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  desktopMq.addEventListener('change', onBreakpointChange)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  desktopMq.removeEventListener('change', onBreakpointChange)
  document.body.style.overflow = ''
})
</script>

<template>
  <header class="app-header">
    <div class="app-header__inner">
      <MascotWalker />

      <div class="app-header__brand">
        <RouterLink to="/" class="app-header__logo">LocalHub</RouterLink>
        <span class="app-header__region">대전·충청</span>
      </div>

      <!-- 데스크톱: 가로 메뉴 -->
      <nav class="app-header__nav">
        <RouterLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="app-header__link"
        >
          {{ link.label }}
        </RouterLink>
        <button type="button" class="app-header__search" aria-label="검색" disabled>
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="9" cy="9" r="6.5" stroke="currentColor" stroke-width="1.5" />
            <line
              x1="13.5"
              y1="13.5"
              x2="18"
              y2="18"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
            />
          </svg>
        </button>
      </nav>

      <!-- 모바일: 햄버거 버튼 -->
      <button
        type="button"
        class="app-header__toggle"
        :aria-expanded="isMenuOpen"
        aria-controls="app-drawer"
        aria-label="메뉴 열기"
        @click="isMenuOpen = true"
      >
        <span class="app-header__toggle-bar" />
        <span class="app-header__toggle-bar" />
        <span class="app-header__toggle-bar" />
      </button>
    </div>

    <!-- 모바일 사이드바 -->
    <Transition name="drawer-fade">
      <div v-if="isMenuOpen" class="drawer-backdrop" @click="closeMenu" />
    </Transition>

    <Transition name="drawer-slide">
      <aside v-if="isMenuOpen" id="app-drawer" class="drawer">
        <div class="drawer__head">
          <span class="drawer__title">메뉴</span>
          <button type="button" class="drawer__close" aria-label="메뉴 닫기" @click="closeMenu">
            ✕
          </button>
        </div>
        <nav class="drawer__nav">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="drawer__link"
          >
            {{ link.label }}
          </RouterLink>
        </nav>
      </aside>
    </Transition>
  </header>
</template>

<style scoped>
.app-header {
  height: 64px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.app-header__inner {
  position: relative; /* 마스코트를 이 영역 기준으로 배치 */
  max-width: 1080px;
  height: 100%;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.app-header__brand {
  position: relative;
  z-index: 1; /* 마스코트가 로고 뒤로 지나가도록 */
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.app-header__logo {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}

.app-header__region {
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.app-header__nav {
  position: relative;
  z-index: 1; /* 마스코트가 메뉴 뒤로 지나가도록 */
  display: flex;
  align-items: center;
  gap: 24px;
}

.app-header__link {
  font-size: var(--font-size-body);
  color: var(--color-text);
  text-decoration: none;
  white-space: nowrap;
}

.app-header__link:hover {
  color: var(--color-primary);
}

.app-header__search {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  padding: 0;
  border: none;
  background: none;
  color: var(--color-text-secondary);
  cursor: default;
}

/* 햄버거 버튼: 데스크톱에서는 숨긴다 */
.app-header__toggle {
  position: relative;
  z-index: 1;
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
}

.app-header__toggle-bar {
  width: 20px;
  height: 2px;
  margin: 0 auto;
  border-radius: 1px;
  background: var(--color-text);
}

/* 사이드바 */
.drawer-backdrop {
  position: fixed;
  inset: 0;
  z-index: 900;
  background: rgba(0, 0, 0, 0.4);
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 901;
  width: min(72vw, 280px);
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.15);
}

.drawer__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 20px;
  border-bottom: 1px solid var(--color-border);
}

.drawer__title {
  font-size: var(--font-size-body);
  font-weight: 600;
  color: var(--color-text);
}

.drawer__close {
  border: none;
  background: none;
  font-size: 18px;
  color: var(--color-text-secondary);
  cursor: pointer;
}

.drawer__nav {
  display: flex;
  flex-direction: column;
  padding: 8px 0;
}

.drawer__link {
  padding: 16px 20px;
  font-size: var(--font-size-body);
  color: var(--color-text);
  text-decoration: none;
}

.drawer__link:hover,
.drawer__link.router-link-active {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.2s ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.25s ease;
}
.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}

/* 모바일: 가로 메뉴를 접고 햄버거로 */
@media (max-width: 768px) {
  .app-header__inner {
    padding: 0 16px;
  }
  .app-header__nav {
    display: none;
  }
  .app-header__toggle {
    display: flex;
  }
}
</style>

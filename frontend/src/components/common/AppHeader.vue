<script setup>
import MascotWalker from './MascotWalker.vue'
</script>

<template>
  <header class="app-header">
    <div class="app-header__inner">
      <MascotWalker />

      <div class="app-header__brand">
        <RouterLink to="/" class="app-header__logo">LocalHub</RouterLink>
        <span class="app-header__region">대전·충청</span>
      </div>

      <nav class="app-header__nav">
        <RouterLink to="/community" class="app-header__link">게시판</RouterLink>
        <RouterLink to="/map" class="app-header__link">지도</RouterLink>
        <RouterLink to="/bread-map" class="app-header__link">빵지순례</RouterLink>
        <RouterLink to="/local-info" class="app-header__link">지역 정보</RouterLink>
        <button
          type="button"
          class="app-header__search"
          aria-label="검색"
          disabled
        >
          <svg
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="9"
              cy="9"
              r="6.5"
              stroke="currentColor"
              stroke-width="1.5"
            />
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
    </div>
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
}

.app-header__link:hover {
  color: var(--color-primary);
}

.app-header__link--disabled {
  color: var(--color-text-secondary);
  cursor: default;
}

.app-header__link--disabled:hover {
  color: var(--color-text-secondary);
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
</style>

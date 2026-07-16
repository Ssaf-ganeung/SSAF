<script setup>
import { ref, onMounted } from 'vue'
import { fetchPosts } from '../api/posts'

// 카테고리 바로가기 (지도 필터는 선택기능이므로 지금은 게시판으로 연결)
const categories = [
  { key: 'tour', label: '관광지', icon: '🏞️' },
  { key: 'food', label: '맛집', icon: '🍜' },
  { key: 'festival', label: '축제·행사', icon: '🎉' },
]

const recentPosts = ref([])
const loading = ref(true)
const loadError = ref(false)

// 최근 게시글 5개 로드 (백엔드 미가동/빈 목록도 안전 처리)
onMounted(async () => {
  try {
    const res = await fetchPosts()
    const list = Array.isArray(res.data) ? res.data : (res.data?.items ?? [])
    recentPosts.value = list.slice(0, 5)
  } catch (err) {
    console.error('[home] 최근 게시글 로드 실패:', err)
    loadError.value = true
  } finally {
    loading.value = false
  }
})

// 날짜를 MM.DD 형식으로
function formatDate(value) {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return ''
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${mm}.${dd}`
}
</script>

<template>
  <div class="home">
    <!-- 1) 히어로 배너 -->
    <section class="hero">
      <h1 class="hero__title">지역 정보 공유 커뮤니티 LocalHub</h1>
      <p class="hero__subtitle">대전·충청 지역 정보를 한눈에 만나보세요</p>
    </section>

    <div class="home__inner">
      <!-- 2) 카테고리 바로가기 -->
      <section class="section">
        <h3 class="section__title">카테고리 바로가기</h3>
        <div class="categories">
          <RouterLink
            v-for="cat in categories"
            :key="cat.key"
            to="/community"
            class="category-card"
          >
            <span class="category-card__icon">{{ cat.icon }}</span>
            <span class="category-card__label">{{ cat.label }}</span>
          </RouterLink>
        </div>
      </section>

      <!-- 3) 최근 게시글 -->
      <section class="section">
        <div class="section__head">
          <h3 class="section__title">최근 게시글</h3>
          <RouterLink to="/community" class="section__more">전체보기 &gt;</RouterLink>
        </div>

        <p v-if="loading" class="state">불러오는 중…</p>
        <p v-else-if="loadError" class="state">게시글을 불러오지 못했어요.</p>
        <p v-else-if="recentPosts.length === 0" class="state">
          아직 게시글이 없습니다. 첫 글을 작성해보세요.
        </p>
        <ul v-else class="post-list">
          <li v-for="post in recentPosts" :key="post.id" class="post-row">
            <RouterLink :to="`/community/${post.id}`" class="post-row__title">
              {{ post.title }}
            </RouterLink>
            <span class="post-row__date">{{ formatDate(post.created_at) }}</span>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* 색상·폰트는 전역 style.css 토큰(--color-*, --font-* )을 사용 */
.home {
  text-align: left;
  color: var(--color-text);
}

/* 히어로 배너 */
.hero {
  background: var(--color-primary-light);
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 32px 16px;
  text-align: center;
}
.hero__title {
  font-size: var(--font-size-h1);
  font-weight: 600;
  color: var(--color-primary);
}
.hero__subtitle {
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
}

/* 콘텐츠 컨테이너 */
.home__inner {
  max-width: 1080px;
  margin: 0 auto;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.section__title {
  font-size: var(--font-size-h3);
  font-weight: 600;
}
.section__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.section__more {
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
}
.section__more:hover {
  color: var(--color-primary);
}

/* 카테고리 카드 3개 */
.categories {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 16px;
}
.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 28px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text);
  text-decoration: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.category-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-card);
}
.category-card__icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-primary-light);
  font-size: 36px;
}
.category-card__label {
  font-size: var(--font-size-body);
  font-weight: 500;
}

/* 최근 게시글 목록 */
.post-list {
  list-style: none;
  margin: 16px 0 0;
  padding: 0;
}
.post-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 4px;
  border-bottom: 1px solid var(--color-border);
}
.post-row__title {
  font-size: var(--font-size-body);
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.post-row__title:hover {
  color: var(--color-primary);
}
.post-row__date {
  flex-shrink: 0;
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.state {
  margin-top: 16px;
  padding: 32px;
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}

/* 모바일: 카테고리 세로 스택 */
@media (max-width: 768px) {
  .categories {
    grid-template-columns: 1fr;
  }
  .home__inner {
    padding: 24px 16px;
    gap: 32px;
  }
}
</style>

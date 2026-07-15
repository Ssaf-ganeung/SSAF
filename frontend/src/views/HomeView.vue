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
/* 컴포넌트 자체 디자인 변수 (나중에 전역 토큰으로 이관하기 쉽게 여기 모음) */
.home {
  --primary: #1d4ed8;
  --primary-hover: #1e3a8a;
  --primary-light: #e4edfd;
  --text: #111827;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
  --surface: #ffffff;
  text-align: left;
  color: var(--text);
  font-family: 'NanumSquare', system-ui, sans-serif;
}

/* 전역 style.css의 h1/h2 폰트 지정을 이겨서 홈 제목도 나눔스퀘어 상속 */
.home :where(h1, h2, h3) {
  font-family: inherit;
}

/* 히어로 배너 */
.hero {
  background: var(--primary-light);
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
  font-size: 28px;
  font-weight: 600;
  color: var(--primary);
}
.hero__subtitle {
  font-size: 14px;
  color: var(--text-secondary);
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
  font-size: 18px;
  font-weight: 600;
}
.section__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.section__more {
  font-size: 14px;
  color: var(--text-secondary);
}
.section__more:hover {
  color: var(--primary);
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
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--text);
  text-decoration: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.category-card:hover {
  border-color: var(--primary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.category-card__icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--primary-light);
  font-size: 36px;
}
.category-card__label {
  font-size: 16px;
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
  border-bottom: 1px solid var(--border);
}
.post-row__title {
  font-size: 16px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.post-row__title:hover {
  color: var(--primary);
}
.post-row__date {
  flex-shrink: 0;
  font-size: 12px;
  color: var(--text-secondary);
}

.state {
  margin-top: 16px;
  padding: 32px;
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
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

<!-- 나눔스퀘어 웹폰트 (Naver, 무료·상업적 이용 가능) — 나중에 전역 style.css로 이관 -->
<style>
@import url('https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@1.0/nanumsquare.css');
</style>

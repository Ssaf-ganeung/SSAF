<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fetchPosts } from '../../api/posts'
import { ALL_CATEGORY, CATEGORY_FILTER_OPTIONS } from '../../constants/postCategories'
import BaseButton from '../../components/common/BaseButton.vue'
import Breadcrumb from '../../components/common/Breadcrumb.vue'
import Pagination from '../../components/common/Pagination.vue'
import PostCard from '../../components/community/PostCard.vue'

const PAGE_SIZE = 10

const breadcrumbItems = [{ label: '홈', to: '/' }, { label: '게시판' }]

const router = useRouter()

const posts = ref([])
const loading = ref(false)
const error = ref(null)
const selectedCategory = ref(ALL_CATEGORY)
const searchInput = ref('')
const searchQuery = ref('')
const currentPage = ref(1)

async function loadPosts() {
  loading.value = true
  error.value = null
  try {
    const res = await fetchPosts({ category: selectedCategory.value })
    posts.value = res.data
  } catch {
    error.value = '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function selectCategory(category) {
  if (category === selectedCategory.value) return
  selectedCategory.value = category
  currentPage.value = 1
  loadPosts()
}

watch(searchQuery, () => {
  currentPage.value = 1
})

function handleSearch() {
  searchQuery.value = searchInput.value
}

const filteredPosts = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return posts.value
  return posts.value.filter(
    (post) =>
      post.title.toLowerCase().includes(query) || post.content.toLowerCase().includes(query)
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredPosts.value.length / PAGE_SIZE)))

const pagedPosts = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredPosts.value.slice(start, start + PAGE_SIZE)
})

function rowNumber(indexInPage) {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredPosts.value.length - start - indexInPage
}

const isSearching = computed(() => searchQuery.value.trim().length > 0)

function goToWrite() {
  router.push('/community/new')
}

onMounted(loadPosts)
</script>

<template>
  <section class="post-list-view">
    <Breadcrumb :items="breadcrumbItems" />

    <div class="post-list-view__categories">
      <button
        v-for="category in CATEGORY_FILTER_OPTIONS"
        :key="category"
        type="button"
        class="post-list-view__category"
        :class="{ 'post-list-view__category--active': category === selectedCategory }"
        @click="selectCategory(category)"
      >
        {{ category }}
      </button>
    </div>

    <div class="post-list-view__toolbar">
      <input
        v-model="searchInput"
        type="text"
        class="post-list-view__search"
        placeholder="게시글 검색어를 입력하세요"
        @keyup.enter="handleSearch"
      />
      <BaseButton variant="dark" @click="handleSearch">검색</BaseButton>
      <BaseButton variant="primary" @click="goToWrite">+ 글쓰기</BaseButton>
    </div>

    <p v-if="loading" class="post-list-view__status">불러오는 중입니다...</p>
    <div v-else-if="error" class="post-list-view__status">
      <p class="post-list-view__error">{{ error }}</p>
      <BaseButton variant="secondary" @click="loadPosts">다시 시도</BaseButton>
    </div>
    <div v-else-if="pagedPosts.length === 0" class="post-list-view__empty">
      <p v-if="isSearching">검색 결과가 없습니다.</p>
      <template v-else>
        <p>아직 게시글이 없습니다. 첫 글을 작성해보세요</p>
        <BaseButton variant="primary" @click="goToWrite">+ 글쓰기</BaseButton>
      </template>
    </div>
    <table v-else class="post-list-view__table">
      <colgroup>
        <col style="width: 80px" />
        <col />
        <col style="width: 120px" />
      </colgroup>
      <thead>
        <tr>
          <th class="post-list-view__th post-list-view__th--number">번호</th>
          <th class="post-list-view__th post-list-view__th--title">제목</th>
          <th class="post-list-view__th post-list-view__th--date">작성일</th>
        </tr>
      </thead>
      <tbody>
        <PostCard
          v-for="(post, index) in pagedPosts"
          :key="post.id"
          :post="post"
          :number="rowNumber(index)"
        />
      </tbody>
    </table>

    <Pagination
      v-if="!loading && !error && totalPages > 1"
      :current-page="currentPage"
      :total-pages="totalPages"
      @update:current-page="currentPage = $event"
    />
  </section>
</template>

<style scoped>
.post-list-view {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-list-view__categories {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.post-list-view__category {
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-family: var(--font-sans);
  font-size: var(--font-size-small);
  cursor: pointer;
  transition: background-color 0.15s, border-color 0.15s, color 0.15s;
}

.post-list-view__category:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.post-list-view__category--active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: var(--color-surface);
}

.post-list-view__toolbar {
  display: flex;
  gap: 8px;
}

.post-list-view__search {
  flex: 1;
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: var(--font-size-body);
}

.post-list-view__search:focus {
  outline: none;
  border-color: var(--color-primary);
}

.post-list-view__status,
.post-list-view__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px 0;
  color: var(--color-text-secondary);
  text-align: center;
}

.post-list-view__error {
  color: var(--color-danger);
}

.post-list-view__table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.post-list-view__th {
  height: 44px;
  padding: 0 12px;
  background: var(--color-table-header-bg);
  color: var(--color-text);
  font-size: var(--font-size-small);
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
}

.post-list-view__th--number {
  text-align: center;
}

.post-list-view__th--title {
  text-align: left;
}

.post-list-view__th--date {
  text-align: right;
}
</style>

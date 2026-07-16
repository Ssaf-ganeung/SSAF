<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { deletePost, fetchPost } from '../../api/posts'
import { formatDate } from '../../utils/date'
import BaseButton from '../../components/common/BaseButton.vue'
import Breadcrumb from '../../components/common/Breadcrumb.vue'
import PasswordConfirmModal from '../../components/community/PasswordConfirmModal.vue'

const props = defineProps({
  id: { type: String, required: true },
})

const breadcrumbItems = [{ label: '홈', to: '/' }, { label: '게시판', to: '/community' }, { label: '게시글 상세' }]

const router = useRouter()

const post = ref(null)
const loading = ref(false)
const error = ref(null)
const modalVisible = ref(false)
const modalError = ref('')

async function loadPost() {
  loading.value = true
  error.value = null
  try {
    const res = await fetchPost(props.id)
    post.value = res.data
  } catch (err) {
    error.value = err.response?.status === 404 ? '게시글을 찾을 수 없습니다' : '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function goToEdit() {
  router.push(`/community/${props.id}/edit`)
}

function openDeleteModal() {
  modalVisible.value = true
  modalError.value = ''
}

async function onDeleteConfirm(password) {
  try {
    await deletePost(props.id, { password })
    modalVisible.value = false
    router.push('/community')
  } catch (err) {
    if (err.response?.status === 403) {
      modalError.value = '비밀번호가 일치하지 않습니다'
    } else if (err.response?.status === 404) {
      modalVisible.value = false
      error.value = '게시글이 이미 삭제되었습니다'
    } else {
      modalError.value = '삭제 중 오류가 발생했습니다'
    }
  }
}

function onModalClose() {
  modalVisible.value = false
  modalError.value = ''
}

onMounted(loadPost)
</script>

<template>
  <section class="post-detail-view">
    <Breadcrumb :items="breadcrumbItems" />

    <p v-if="loading" class="post-detail-view__status">불러오는 중입니다...</p>
    <div v-else-if="error" class="post-detail-view__status">
      <p class="post-detail-view__error">{{ error }}</p>
      <BaseButton variant="secondary" @click="router.push('/community')">목록으로</BaseButton>
    </div>
    <template v-else-if="post">
      <div class="post-detail-view__head">
        <h2>{{ post.title }}</h2>
        <span class="post-detail-view__date">작성일 {{ formatDate(post.created_at) }}</span>
      </div>
      <div class="post-detail-view__content">{{ post.content }}</div>
      <div class="post-detail-view__actions">
        <BaseButton variant="secondary" @click="goToEdit">수정</BaseButton>
        <BaseButton variant="danger-outline" @click="openDeleteModal">삭제</BaseButton>
      </div>
    </template>

    <PasswordConfirmModal
      :visible="modalVisible"
      :error-message="modalError"
      @confirm="onDeleteConfirm"
      @close="onModalClose"
    />
  </section>
</template>

<style scoped>
.post-detail-view {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-detail-view__status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 0;
  color: var(--color-text-secondary);
  text-align: center;
}

.post-detail-view__error {
  color: var(--color-danger);
}

.post-detail-view__head {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.post-detail-view__date {
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}

.post-detail-view__content {
  min-height: 300px;
  white-space: pre-wrap;
  color: var(--color-text);
  font-size: var(--font-size-body);
  line-height: 1.7;
}

.post-detail-view__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>

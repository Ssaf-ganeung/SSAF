<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { createPost, fetchPost, updatePost } from '../../api/posts'
import PostForm from '../../components/community/PostForm.vue'
import BaseButton from '../../components/common/BaseButton.vue'
import Breadcrumb from '../../components/common/Breadcrumb.vue'

const props = defineProps({
  id: { type: String, required: false, default: null },
})

const router = useRouter()

const isEdit = computed(() => props.id !== null)

const breadcrumbItems = computed(() => [
  { label: '홈', to: '/' },
  { label: '게시판', to: '/community' },
  { label: isEdit.value ? '게시글 수정' : '글쓰기' },
])

const form = ref({ title: '', content: '', category: '', password: '' })

const loading = ref(false)
const submitting = ref(false)
const loadError = ref(null)
const submitError = ref(null)

async function loadPost() {
  loading.value = true
  loadError.value = null
  try {
    const res = await fetchPost(props.id)
    form.value.title = res.data.title
    form.value.content = res.data.content
    form.value.category = res.data.category
  } catch {
    loadError.value = '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  submitting.value = true
  submitError.value = null
  try {
    if (isEdit.value) {
      await updatePost(props.id, { ...form.value })
      router.push(`/community/${props.id}`)
    } else {
      const res = await createPost({ ...form.value })
      router.push(`/community/${res.data.id}`)
    }
  } catch (err) {
    if (isEdit.value && err.response?.status === 403) {
      submitError.value = '비밀번호가 일치하지 않습니다'
    } else {
      submitError.value = '요청 처리 중 오류가 발생했습니다.'
    }
  } finally {
    submitting.value = false
  }
}

function handleCancel() {
  router.push(isEdit.value ? `/community/${props.id}` : '/community')
}

onMounted(() => {
  if (isEdit.value) loadPost()
})
</script>

<template>
  <section class="post-form-view">
    <Breadcrumb :items="breadcrumbItems" />
    <h2>{{ isEdit ? '게시글 수정' : '게시글 작성' }}</h2>

    <p v-if="loading" class="post-form-view__status">불러오는 중입니다...</p>
    <div v-else-if="loadError" class="post-form-view__status">
      <p class="post-form-view__error">{{ loadError }}</p>
      <BaseButton variant="secondary" @click="router.push('/community')">목록으로</BaseButton>
    </div>
    <PostForm
      v-else
      v-model="form"
      :mode="isEdit ? 'edit' : 'create'"
      :server-error="submitError"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </section>
</template>

<style scoped>
.post-form-view {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-form-view__status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 0;
  color: var(--color-text-secondary);
  text-align: center;
}

.post-form-view__error {
  color: var(--color-danger);
}
</style>

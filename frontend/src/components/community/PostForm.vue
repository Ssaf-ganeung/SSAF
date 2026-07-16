<script setup>
import { reactive } from 'vue'
import BaseButton from '../common/BaseButton.vue'
import { POST_CATEGORIES } from '../../constants/postCategories'

const props = defineProps({
  modelValue: { type: Object, required: true },
  mode: { type: String, default: 'create', validator: (value) => ['create', 'edit'].includes(value) },
  serverError: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])

const errors = reactive({ title: '', category: '', content: '', password: '' })

function update(field, value) {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}

function validate() {
  errors.title = props.modelValue.title.trim().length >= 1 && props.modelValue.title.trim().length <= 100
    ? ''
    : '제목을 입력해주세요'
  errors.category = props.modelValue.category ? '' : '카테고리를 선택해주세요'
  errors.content = props.modelValue.content.trim().length >= 1 ? '' : '내용을 입력해주세요'
  const passwordLength = props.modelValue.password.length
  errors.password = passwordLength >= 4 && passwordLength <= 20 ? '' : '비밀번호는 4~20자로 입력해주세요'

  return !errors.title && !errors.category && !errors.content && !errors.password
}

function handleSubmit() {
  if (!validate()) return
  emit('submit')
}
</script>

<template>
  <form class="post-form" @submit.prevent="handleSubmit">
    <div class="post-form__field">
      <label for="post-title">제목</label>
      <input
        id="post-title"
        type="text"
        class="post-form__input post-form__input--title"
        :class="{ 'post-form__input--error': errors.title }"
        maxlength="100"
        :value="modelValue.title"
        @input="update('title', $event.target.value)"
      />
      <p v-if="errors.title" class="post-form__error">{{ errors.title }}</p>
    </div>

    <div class="post-form__field">
      <label for="post-category">카테고리</label>
      <select
        id="post-category"
        class="post-form__input post-form__input--title"
        :value="modelValue.category"
        @change="update('category', $event.target.value)"
      >
        <option value="" disabled>카테고리 선택</option>
        <option v-for="category in POST_CATEGORIES" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <p v-if="errors.category" class="post-form__error">{{ errors.category }}</p>
    </div>

    <div class="post-form__field">
      <label for="post-content">내용</label>
      <textarea
        id="post-content"
        class="post-form__input post-form__textarea"
        :value="modelValue.content"
        @input="update('content', $event.target.value)"
      ></textarea>
      <p v-if="errors.content" class="post-form__error">{{ errors.content }}</p>
    </div>

    <div class="post-form__field">
      <label for="post-password">수정용 비밀번호</label>
      <div class="post-form__password-row">
        <input
          id="post-password"
          type="password"
          class="post-form__input post-form__input--password"
          maxlength="20"
          :value="modelValue.password"
          @input="update('password', $event.target.value)"
        />
        <p class="post-form__help">※ 게시글 수정·삭제 시 확인용으로 사용됩니다 (평문 저장)</p>
      </div>
      <p v-if="errors.password" class="post-form__error">{{ errors.password }}</p>
      <p v-if="serverError" class="post-form__error">{{ serverError }}</p>
    </div>

    <div class="post-form__actions">
      <BaseButton variant="secondary" @click="$emit('cancel')">취소</BaseButton>
      <BaseButton variant="primary" @click="handleSubmit">{{ mode === 'edit' ? '저장' : '등록' }}</BaseButton>
    </div>
  </form>
</template>

<style scoped>
.post-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.post-form__field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.post-form__field label {
  color: var(--color-text);
  font-size: var(--font-size-small);
  font-weight: 600;
}

.post-form__input {
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: var(--font-size-body);
  color: var(--color-text);
  background: var(--color-surface);
}

.post-form__input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.post-form__input--error {
  border-color: var(--color-danger);
}

.post-form__input--title {
  height: 44px;
  width: 100%;
}

.post-form__textarea {
  height: 320px;
  width: 100%;
  resize: vertical;
}

.post-form__password-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.post-form__input--password {
  height: 44px;
  width: 320px;
  flex-shrink: 0;
}

.post-form__help {
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}

.post-form__error {
  color: var(--color-danger);
  font-size: var(--font-size-caption);
}

.post-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>

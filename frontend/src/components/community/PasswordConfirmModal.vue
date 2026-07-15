<script setup>
import { ref } from 'vue'
import BaseButton from '../common/BaseButton.vue'

defineProps({
  visible: { type: Boolean, default: false },
  errorMessage: { type: String, default: '' },
})

const emit = defineEmits(['confirm', 'close'])

const password = ref('')

function handleConfirm() {
  if (!password.value) return
  emit('confirm', password.value)
  password.value = ''
}

function handleClose() {
  password.value = ''
  emit('close')
}
</script>

<template>
  <div v-if="visible" class="password-confirm-modal__backdrop" @click.self="handleClose">
    <div class="password-confirm-modal__panel">
      <div class="password-confirm-modal__header">
        <h3>비밀번호 확인</h3>
        <button type="button" class="password-confirm-modal__close" aria-label="닫기" @click="handleClose">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <line x1="5" y1="5" x2="15" y2="15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            <line x1="15" y1="5" x2="5" y2="15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </button>
      </div>
      <input
        v-model="password"
        type="password"
        class="password-confirm-modal__input"
        :class="{ 'password-confirm-modal__input--error': errorMessage }"
        placeholder="수정용 비밀번호 입력"
        @keyup.enter="handleConfirm"
      />
      <p v-if="errorMessage" class="password-confirm-modal__error">{{ errorMessage }}</p>
      <BaseButton variant="primary" class="password-confirm-modal__confirm" @click="handleConfirm">확인</BaseButton>
    </div>
  </div>
</template>

<style scoped>
.password-confirm-modal__backdrop {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  z-index: 100;
}

.password-confirm-modal__panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 360px;
  padding: 24px;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  box-shadow: var(--shadow-card);
}

.password-confirm-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.password-confirm-modal__header h3 {
  font-size: 16px;
  font-weight: 600;
}

.password-confirm-modal__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  padding: 0;
  border: none;
  background: none;
  color: var(--color-text-secondary);
  cursor: pointer;
}

.password-confirm-modal__close:hover {
  color: var(--color-text);
}

.password-confirm-modal__input {
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: var(--font-size-body);
}

.password-confirm-modal__input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.password-confirm-modal__input--error {
  border-color: var(--color-danger);
}

.password-confirm-modal__error {
  color: var(--color-danger);
  font-size: var(--font-size-caption);
}

.password-confirm-modal__confirm {
  width: 100%;
}
</style>

<script setup>
defineProps({
  visible: { type: Boolean, default: false },
})
defineEmits(['confirm', 'close'])
// TODO: 수정/삭제 요청 시 비밀번호 입력받아 서버에 평문 비교 요청
</script>

<template>
  <div v-if="visible" class="password-confirm-modal">
    <p>비밀번호 확인 (추후 구현)</p>
  </div>
</template>

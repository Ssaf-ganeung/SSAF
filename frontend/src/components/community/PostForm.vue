<script setup>
defineProps({
  modelValue: { type: Object, required: true },
})
defineEmits(['update:modelValue', 'submit'])
// TODO: 제목/내용/비밀번호 입력 필드 및 유효성 검사 구현
</script>

<template>
  <form @submit.prevent="$emit('submit')">
    <p>게시글 작성 폼 (추후 구현: 제목 / 내용 / 비밀번호)</p>
  </form>
</template>

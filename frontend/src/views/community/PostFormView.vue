<script setup>
defineProps({
  id: { type: String, required: false, default: null },
})
// TODO: id 존재 여부에 따라 작성/수정 모드 분기, PostForm 컴포넌트로 createPost/updatePost 연동
</script>

<template>
  <section>
    <h2>게시글 작성/수정</h2>
    <p>작성·수정 폼 (추후 구현)</p>
  </section>
</template>

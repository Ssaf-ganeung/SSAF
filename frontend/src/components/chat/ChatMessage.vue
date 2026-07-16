<script setup>
defineProps({
  role: {
    type: String,
    required: true,
  },
  content: {
    type: String,
    required: true,
  },
  relatedPlaces: {
    type: Array,
    default: () => [],
  },
});
</script>

<template>
  <div :class="['chat-message', role]">
    <p class="chat-message__content">
      {{ content }}
    </p>

    <div
      v-if="role === 'assistant' && relatedPlaces.length"
      class="chat-message__places"
    >
      <RouterLink
        v-for="place in relatedPlaces"
        :key="`${place.content_type_id}:${place.id}`"
        :to="{
          name: 'map',
          query: {
            place_id: place.id,
            content_type_id: place.content_type_id,
          },
        }"
        class="chat-message__map-link"
      >
        {{ place.title }} 지도에서 보기
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.chat-message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap; /* 줄바꿈 유지 */
  word-break: break-word;
}

/* 사용자 말풍선: 오른쪽, 파란색 */
.chat-message.user {
  align-self: flex-end;
  background: #2f6fed;
  color: #fff;
  border-bottom-right-radius: 2px;
}

/* 봇 말풍선: 왼쪽, 흰색 */
.chat-message.assistant {
  align-self: flex-start;
  background: #fff;
  color: #222;
  border: 1px solid #e3e6ea;
  border-bottom-left-radius: 2px;
}

.chat-message__content {
  margin: 0;
  white-space: pre-wrap;
}

.chat-message__places {
  display: grid;
  gap: 6px;
  margin-top: 10px;
}

.chat-message__map-link {
  padding: 7px 9px;
  color: #004346;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  background: rgba(117, 221, 221, 0.2);
  border: 1px solid #09bc8a;
  border-radius: 7px;
}

.chat-message__map-link:hover {
  color: #fff;
  background: #004346;
}
</style>

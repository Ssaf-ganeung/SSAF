<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  place: { type: Object, required: true },
});

const TYPE_EMOJIS = {
  관광지: "🏞️",
  문화시설: "🏛️",
  축제공연행사: "🎉",
  여행코스: "🧭",
  레포츠: "🚵",
  숙박: "🏨",
  쇼핑: "🛍️",
  음식점: "🍽️",
};

const imageFailed = ref(false);

// 카테고리 전환 시 컴포넌트가 재사용되므로 실패 상태를 초기화한다
watch(
  () => props.place,
  () => {
    imageFailed.value = false;
  },
);
</script>

<template>
  <article class="place-card">
    <div class="place-card__media">
      <img
        v-if="place.image_url && !imageFailed"
        :src="place.image_url"
        :alt="place.title"
        class="place-card__image"
        loading="lazy"
        @error="imageFailed = true"
      />

      <div v-else class="place-card__placeholder" aria-hidden="true">
        <span class="place-card__placeholder-icon">
          {{ TYPE_EMOJIS[place.content_type] || "📍" }}
        </span>
        <span class="place-card__placeholder-text">이미지를 불러올 수 없습니다</span>
      </div>
    </div>

    <div class="place-card__body">
      <h3 class="place-card__title">{{ place.title }}</h3>

      <p v-if="place.address" class="place-card__address">
        {{ place.address }}
      </p>

      <p v-else class="place-card__address place-card__address--empty">
        주소 정보 없음
      </p>
    </div>
  </article>
</template>

<style scoped>
.place-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.place-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-card);
}

.place-card__media {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: var(--color-primary-light);
}

.place-card__image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.place-card__placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.place-card__placeholder-icon {
  font-size: 32px;
}

.place-card__placeholder-text {
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.place-card__body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px;
}

.place-card__title {
  margin: 0;
  font-size: var(--font-size-h3);
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.place-card__address {
  margin: 0;
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
}

.place-card__address--empty {
  font-style: italic;
  opacity: 0.7;
}
</style>

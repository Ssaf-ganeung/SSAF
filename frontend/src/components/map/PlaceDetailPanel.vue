<script setup>
import { computed, ref, watch } from "vue";

import { PLACE_TYPE_MAP } from "../../constants/placeTypes";

const props = defineProps({
  place: {
    type: Object,
    required: true,
  },

  isFavorite: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["close", "toggle-favorite"]);

const imageFailed = ref(false);

const markerImage = computed(
  () => PLACE_TYPE_MAP[props.place.content_type_id]?.icon.iconUrl,
);

const hasImage = computed(
  () => Boolean(props.place.image_url) && !imageFailed.value,
);

const phoneHref = computed(() => {
  const phoneNumber = String(props.place.telephone ?? "").replace(
    /[^0-9+]/g,
    "",
  );

  return phoneNumber ? `tel:${phoneNumber}` : "";
});

const encodedPlaceName = computed(() => encodeURIComponent(props.place.title));

const kakaoMapUrl = computed(
  () =>
    `https://map.kakao.com/link/map/${encodedPlaceName.value},${props.place.latitude},${props.place.longitude}`,
);

const kakaoDirectionsUrl = computed(
  () =>
    `https://map.kakao.com/link/to/${encodedPlaceName.value},${props.place.latitude},${props.place.longitude}`,
);

watch(
  () => props.place.id,
  () => {
    imageFailed.value = false;
  },
);
</script>

<template>
  <aside class="place-detail" aria-labelledby="place-detail-title">
    <button
      type="button"
      class="place-detail__close"
      aria-label="장소 상세 닫기"
      @click="$emit('close')"
    >
      ×
    </button>

    <img
      v-if="hasImage"
      :src="place.image_url"
      :alt="`${place.title} 대표 이미지`"
      class="place-detail__image"
      @error="imageFailed = true"
    />

    <div v-else class="place-detail__image-placeholder">
      <img
        v-if="markerImage"
        :src="markerImage"
        alt=""
        class="place-detail__marker-image"
      />

      <span>등록된 대표 이미지가 없습니다.</span>
    </div>

    <div class="place-detail__body">
      <span class="place-detail__type">
        {{ place.content_type }}
      </span>

      <h2 id="place-detail-title" class="place-detail__title">
        {{ place.title }}
      </h2>
      <button
        type="button"
        class="place-detail__favorite"
        :aria-pressed="isFavorite"
        @click="$emit('toggle-favorite')"
      >
        <span aria-hidden="true">
          {{ isFavorite ? "★" : "☆" }}
        </span>

        {{ isFavorite ? "즐겨찾기 해제" : "즐겨찾기 추가" }}
      </button>

      <dl class="place-detail__information">
        <div v-if="place.address" class="place-detail__row">
          <dt>주소</dt>
          <dd>{{ place.address }}</dd>
        </div>

        <div v-if="place.telephone" class="place-detail__row">
          <dt>전화</dt>
          <dd>
            <a :href="phoneHref">
              {{ place.telephone }}
            </a>
          </dd>
        </div>

        <div class="place-detail__row">
          <dt>권역</dt>
          <dd>{{ place.region }}</dd>
        </div>
      </dl>

      <div class="place-detail__actions">
        <a
          :href="kakaoMapUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="place-detail__action place-detail__action--primary"
        >
          카카오맵에서 보기
        </a>

        <a
          :href="kakaoDirectionsUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="place-detail__action"
        >
          길찾기
        </a>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.place-detail {
  position: relative;
  overflow: hidden;
  color: #172a3a;
  background: #fff;
  border: 1px solid #75dddd;
  border-radius: 12px;
  box-shadow: 0 14px 32px rgba(23, 42, 58, 0.16);
}

.place-detail__close {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
  width: 32px;
  height: 32px;
  padding: 0;
  color: #172a3a;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.92);
  border: 0;
  border-radius: 50%;
}

.place-detail__image,
.place-detail__image-placeholder {
  width: 100%;
  height: 220px;
}

.place-detail__image {
  display: block;
  object-fit: cover;
}

.place-detail__image-placeholder {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  justify-content: center;
  color: #508991;
  font-size: 13px;
  background: rgba(117, 221, 221, 0.2);
}

.place-detail__marker-image {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.place-detail__body {
  padding: 20px;
}

.place-detail__type {
  display: inline-flex;
  padding: 4px 9px;
  margin-bottom: 10px;
  color: #004346;
  font-size: 12px;
  font-weight: 700;
  background: #75dddd;
  border-radius: 999px;
}

.place-detail__title {
  margin: 0;
  color: #172a3a;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.35;
}

.place-detail__information {
  display: grid;
  gap: 12px;
  margin: 20px 0;
}

.place-detail__row {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 10px;
}

.place-detail__row dt {
  color: #508991;
  font-size: 13px;
  font-weight: 700;
}

.place-detail__row dd {
  min-width: 0;
  margin: 0;
  overflow-wrap: anywhere;
  font-size: 14px;
  line-height: 1.5;
}

.place-detail__row a {
  color: #004346;
}

.place-detail__actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.place-detail__action {
  padding: 10px 12px;
  color: #004346;
  font-size: 13px;
  font-weight: 700;
  text-align: center;
  text-decoration: none;
  border: 1px solid #09bc8a;
  border-radius: 8px;
}

.place-detail__action--primary {
  color: #fff;
  background: #004346;
  border-color: #004346;
}

.place-detail__favorite {
  display: inline-flex;
  gap: 6px;
  align-items: center;
  padding: 8px 10px;
  margin-top: 12px;
  color: #004346;
  font-weight: 700;
  cursor: pointer;
  background: rgba(117, 221, 221, 0.2);
  border: 1px solid #09bc8a;
  border-radius: 8px;
}

.place-detail__favorite[aria-pressed="true"] {
  color: #fff;
  background: #004346;
}
</style>

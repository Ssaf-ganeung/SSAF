<script setup>
import { computed, onMounted, ref, watch } from "vue";

import { getPlaces } from "../api/places";
import CategoryTabs from "../components/localInfo/CategoryTabs.vue";
import PlaceCard from "../components/localInfo/PlaceCard.vue";

const places = ref([]);
const selectedTypeId = ref("12");
const loading = ref(false);
const error = ref("");

// 원본 데이터에 이미지가 없는 항목은 카드 목록에서 제외한다
const visiblePlaces = computed(() =>
  places.value.filter((place) => place.image_url),
);

let requestSequence = 0;

async function fetchPlaces() {
  const currentRequest = ++requestSequence;

  loading.value = true;
  error.value = "";

  try {
    const response = await getPlaces({
      content_type_id: selectedTypeId.value,
    });

    if (currentRequest !== requestSequence) {
      return;
    }

    places.value = response.data;
  } catch (requestError) {
    if (currentRequest !== requestSequence) {
      return;
    }

    console.error(requestError);
    error.value = "장소 정보를 불러오지 못했습니다.";
  } finally {
    if (currentRequest === requestSequence) {
      loading.value = false;
    }
  }
}

watch(selectedTypeId, fetchPlaces);

onMounted(fetchPlaces);
</script>

<template>
  <section class="local-info">
    <header class="local-info__header">
      <h1 class="local-info__title">지역 정보</h1>

      <p class="local-info__subtitle">
        대전·충청권의 관광지, 축제, 맛집 정보를 한눈에 확인하세요.
      </p>
    </header>

    <CategoryTabs v-model="selectedTypeId" :disabled="loading" />

    <div class="local-info__result" aria-live="polite">
      <p v-if="loading">장소 정보를 불러오는 중입니다.</p>

      <p v-else-if="error" class="local-info__error">
        {{ error }}
      </p>

      <p v-else>조회 결과 {{ visiblePlaces.length }}개</p>
    </div>

    <p
      v-if="!loading && !error && visiblePlaces.length === 0"
      class="local-info__empty"
    >
      선택한 카테고리에 해당하는 장소가 없습니다.
    </p>

    <div v-else class="local-info__grid">
      <PlaceCard
        v-for="place in visiblePlaces"
        :key="`${place.content_type_id}:${place.id}`"
        :place="place"
      />
    </div>
  </section>
</template>

<style scoped>
.local-info {
  max-width: 1080px;
  margin: 0 auto;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.local-info__header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.local-info__title {
  margin: 0;
  font-size: var(--font-size-h1);
  color: var(--color-text);
}

.local-info__subtitle {
  margin: 0;
  font-size: var(--font-size-body);
  color: var(--color-text-secondary);
}

.local-info__result {
  min-height: 24px;
  font-size: var(--font-size-small);
  color: var(--color-accent-cyan);
}

.local-info__result p {
  margin: 0;
}

.local-info__error {
  color: var(--color-danger);
}

.local-info__empty {
  margin: 0;
  padding: 48px 20px;
  color: var(--color-text-secondary);
  text-align: center;
  background: var(--color-surface);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-md);
}

.local-info__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

@media (max-width: 480px) {
  .local-info {
    padding: 24px 16px;
  }

  .local-info__grid {
    grid-template-columns: 1fr;
  }
}
</style>

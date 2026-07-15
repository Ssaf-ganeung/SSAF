<script setup>
import { onMounted, ref, watch } from "vue";

import { getPlaces } from "../api/places";
import LeafletMap from "../components/map/LeafletMap.vue";
import MapFilter from "../components/map/MapFilter.vue";

const places = ref([]);
const selectedContentTypeId = ref("");
const selectedRegion = ref("");
const loading = ref(false);
const error = ref("");

let requestSequence = 0;

function createRequestParams() {
  const params = {};

  if (selectedContentTypeId.value) {
    params.content_type_id = selectedContentTypeId.value;
  }

  if (selectedRegion.value) {
    params.region = selectedRegion.value;
  }

  return params;
}

async function fetchPlaces() {
  const currentRequest = ++requestSequence;

  loading.value = true;
  error.value = "";

  try {
    const response = await getPlaces(createRequestParams());

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

watch([selectedContentTypeId, selectedRegion], fetchPlaces);

onMounted(fetchPlaces);
</script>

<template>
  <section class="map-view">
    <header class="map-view__header">
      <h1>대전·충청권 지도</h1>

      <p>지역 관광 정보를 지도에서 확인하세요.</p>
    </header>

    <MapFilter
      v-model:content-type-id="selectedContentTypeId"
      v-model:region="selectedRegion"
      :disabled="loading"
    />

    <div class="map-view__result" aria-live="polite">
      <p v-if="loading">장소 정보를 불러오는 중입니다.</p>

      <p v-else-if="error" class="map-view__error">
        {{ error }}
      </p>

      <p v-else>조회 결과 {{ places.length }}개</p>
    </div>

    <p v-if="!loading && !error && places.length === 0" class="map-view__empty">
      선택한 조건에 해당하는 장소가 없습니다.
    </p>

    <LeafletMap v-else :places="places" />
  </section>
</template>

<style scoped>
.map-view {
  padding: 32px;
  text-align: left;
}

.map-view__header {
  margin-bottom: 24px;
}

.map-view__header h1 {
  margin-top: 0;
}

.map-view__result {
  min-height: 24px;
  margin-bottom: 12px;
  color: #508991;
  font-size: 14px;
}

.map-view__result p {
  margin: 0;
}

.map-view__error {
  color: #d14343;
}

.map-view__empty {
  padding: 48px 20px;
  color: #508991;
  text-align: center;
  background: rgba(117, 221, 221, 0.12);
  border: 1px dashed #508991;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .map-view {
    padding: 20px;
  }
}
</style>

<script setup>
import { onMounted, ref, watch, computed } from "vue";

import { getPlaces } from "../api/places";
import { useFavorites } from "../composables/useFavorites";
import LeafletMap from "../components/map/LeafletMap.vue";
import MapFilter from "../components/map/MapFilter.vue";
import PlaceDetailPanel from "../components/map/PlaceDetailPanel.vue";

const places = ref([]);
const selectedContentTypeId = ref("");
const selectedRegion = ref("");
const loading = ref(false);
const error = ref("");
const selectedPlace = ref(null);

const { favoriteCount, isFavorite, toggleFavorite } = useFavorites();

const favoritePlaces = computed(() =>
  places.value.filter((place) => isFavorite(place)),
);

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

function selectPlace(place) {
  selectedPlace.value = place;
}

function closePlaceDetail() {
  selectedPlace.value = null;
}

function isSamePlace(firstPlace, secondPlace) {
  return (
    firstPlace.id === secondPlace.id &&
    firstPlace.content_type_id === secondPlace.content_type_id
  );
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

    if (
      selectedPlace.value &&
      !places.value.some((place) => isSamePlace(place, selectedPlace.value))
    ) {
      selectedPlace.value = null;
    }
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
      <p class="map-view__favorite-count">즐겨찾기 {{ favoriteCount }}개</p>
      <div v-if="favoritePlaces.length" class="map-view__favorites">
        <h2>내 즐겨찾기</h2>

        <button
          v-for="place in favoritePlaces"
          :key="`${place.content_type_id}:${place.id}`"
          type="button"
          class="map-view__favorite-item"
          @click="selectPlace(place)"
        >
          <span>{{ place.title }}</span>
          <small>{{ place.region }} · {{ place.content_type }}</small>
        </button>
      </div>

      <p v-else class="map-view__favorites-empty">
        추가한 즐겨찾기가 없습니다.
      </p>
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

    <div v-else class="map-view__content">
      <div class="map-view__map">
        <LeafletMap :places="places" @select-place="selectPlace" />
      </div>

      <PlaceDetailPanel
        v-if="selectedPlace"
        :place="selectedPlace"
        :is-favorite="isFavorite(selectedPlace)"
        class="map-view__detail"
        @close="closePlaceDetail"
        @toggle-favorite="toggleFavorite(selectedPlace)"
      />
    </div>
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

.map-view__content {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  gap: 20px;
  align-items: start;
}

.map-view__map {
  min-width: 0;
}

.map-view__detail {
  position: sticky;
  top: 20px;
}

@media (max-width: 960px) {
  .map-view__content {
    grid-template-columns: 1fr;
  }

  .map-view__detail {
    position: static;
  }
}

@media (max-width: 768px) {
  .map-view {
    padding: 20px;
  }
}

.map-view__favorite-count {
  color: #004346;
  font-size: 14px;
  font-weight: 700;
}
.map-view__favorites {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.map-view__favorites h2 {
  width: 100%;
  margin: 0 0 4px;
  color: #172a3a;
  font-size: 16px;
}

.map-view__favorite-item {
  display: grid;
  gap: 3px;
  padding: 8px 12px;
  color: #172a3a;
  text-align: left;
  cursor: pointer;
  background: rgba(117, 221, 221, 0.2);
  border: 1px solid #09bc8a;
  border-radius: 8px;
}

.map-view__favorite-item small {
  color: #508991;
}

.map-view__favorites-empty {
  color: #508991;
  font-size: 13px;
}
</style>

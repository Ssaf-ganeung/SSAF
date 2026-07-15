<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { FALLBACK_ICON_OPTIONS, PLACE_TYPES } from "../../constants/placeTypes";

const props = defineProps({
  places: {
    type: Array,
    default: () => [],
  },
});

const PLACE_ICONS = Object.fromEntries(
  PLACE_TYPES.map((placeType) => [placeType.id, L.icon(placeType.icon)]),
);

const FALLBACK_ICON = L.icon(FALLBACK_ICON_OPTIONS);

const DEFAULT_CENTER = [36.5, 127.5];
const DEFAULT_ZOOM = 8;
const MAX_FIT_ZOOM = 14;

const mapContainer = ref(null);

let map = null;
let markerLayer = null;

function getMarkerIcon(contentTypeId) {
  return PLACE_ICONS[contentTypeId] ?? FALLBACK_ICON;
}

function createTextElement(tagName, className, text) {
  const element = document.createElement(tagName);

  element.className = className;
  element.textContent = text;

  return element;
}

function createPopupContent(place) {
  const popup = document.createElement("article");
  popup.className = "place-popup";

  if (place.image_url) {
    const image = document.createElement("img");

    image.className = "place-popup__image";
    image.src = place.image_url;
    image.alt = `${place.title} 대표 이미지`;
    image.loading = "lazy";

    image.addEventListener("error", () => {
      image.remove();
    });

    popup.appendChild(image);
  }

  const body = document.createElement("div");
  body.className = "place-popup__body";

  const type = createTextElement(
    "span",
    "place-popup__type",
    place.content_type,
  );

  const title = createTextElement("h3", "place-popup__title", place.title);

  body.appendChild(type);
  body.appendChild(title);

  if (place.address) {
    const address = createTextElement(
      "p",
      "place-popup__address",
      place.address,
    );

    body.appendChild(address);
  }

  if (place.telephone) {
    const telephone = createTextElement(
      "p",
      "place-popup__telephone",
      `전화 ${place.telephone}`,
    );

    body.appendChild(telephone);
  }

  popup.appendChild(body);

  return popup;
}

function renderMarkers() {
  if (!map || !markerLayer) {
    return;
  }

  markerLayer.clearLayers();

  const bounds = [];

  props.places.forEach((place) => {
    const latitude = Number(place.latitude);
    const longitude = Number(place.longitude);

    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
      return;
    }

    const markerIcon = getMarkerIcon(place.content_type_id);

    const marker = L.marker([latitude, longitude], {
      icon: markerIcon,
      title: place.title,
    });

    marker.bindPopup(createPopupContent(place), {
      minWidth: 220,
      maxWidth: 280,
      autoPanPadding: [20, 20],
    });

    marker.addTo(markerLayer);

    bounds.push([latitude, longitude]);
  });

  if (bounds.length === 0) {
    map.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
    return;
  }

  map.fitBounds(bounds, {
    padding: [30, 30],
    maxZoom: MAX_FIT_ZOOM,
  });
}

onMounted(() => {
  map = L.map(mapContainer.value, {
    preferCanvas: true,
  }).setView(DEFAULT_CENTER, DEFAULT_ZOOM);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  markerLayer = L.layerGroup().addTo(map);

  renderMarkers();
});

watch(() => props.places, renderMarkers);

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
    markerLayer = null;
  }
});
</script>

<template>
  <div class="map-wrapper">
    <div
      ref="mapContainer"
      class="leaflet-map"
      aria-label="대전·충청권 장소 지도"
    ></div>

    <ul class="map-legend" aria-label="장소 유형 범례">
      <li
        v-for="placeType in PLACE_TYPES"
        :key="placeType.id"
        class="map-legend__item"
      >
        <img
          :src="placeType.icon.iconUrl"
          :alt="`${placeType.name} 마커`"
          class="map-legend__icon"
        />

        <span>{{ placeType.name }}</span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.map-wrapper {
  width: 100%;
}

.leaflet-map {
  width: 100%;
  height: 600px;
  min-height: 400px;
  border: 1px solid var(--border);
  border-radius: 8px;
}

.map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 20px;
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.map-legend__item {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 14px;
}

.map-legend__icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.map-wrapper :deep(.leaflet-popup-content-wrapper) {
  padding: 0;
  overflow: hidden;
  border-radius: 12px;
}

.map-wrapper :deep(.leaflet-popup-content) {
  width: auto !important;
  margin: 0;
}

.map-wrapper :deep(.place-popup) {
  width: 260px;
  color: #172a3a;
  background: #fff;
}

.map-wrapper :deep(.place-popup__image) {
  display: block;
  width: 100%;
  height: 150px;
  object-fit: cover;
  background: #e8f7f7;
}

.map-wrapper :deep(.place-popup__body) {
  padding: 16px;
}

.map-wrapper :deep(.place-popup__type) {
  display: inline-flex;
  padding: 3px 8px;
  margin-bottom: 8px;
  color: #004346;
  font-size: 12px;
  font-weight: 700;
  background: #75dddd;
  border-radius: 999px;
}

.map-wrapper :deep(.place-popup__title) {
  margin: 0 0 8px;
  color: #172a3a;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.3;
}

.map-wrapper :deep(.place-popup__address),
.map-wrapper :deep(.place-popup__telephone) {
  margin: 0;
  color: #508991;
  font-size: 13px;
  line-height: 1.5;
}

.map-wrapper :deep(.place-popup__telephone) {
  margin-top: 6px;
  color: #004346;
  font-weight: 600;
}

@media (max-width: 768px) {
  .leaflet-map {
    height: 500px;
  }
}
</style>

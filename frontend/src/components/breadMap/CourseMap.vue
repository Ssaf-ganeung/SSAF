<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  stops: { type: Array, required: true },
  selectedOrder: { type: Number, default: null },
})

const emit = defineEmits(['select'])

const mapContainer = ref(null)

let map = null
let markerLayer = null
let markersByOrder = new Map()

// 순번이 적힌 물방울형 핀 (divIcon + 인라인 SVG)
function createPinIcon(order, selected) {
  return L.divIcon({
    className: 'bread-pin-icon',
    html: `
      <svg class="bread-pin${selected ? ' bread-pin--selected' : ''}" viewBox="-16 -46 32 48" width="32" height="48" aria-hidden="true">
        <path class="bread-pin__shape" d="M0 0C-3 -9 -14 -14.5 -14 -26a14 14 0 1 1 28 0C14 -14.5 3 -9 0 0Z"/>
        <circle class="bread-pin__badge" cx="0" cy="-26" r="9.5"/>
        <text class="bread-pin__order" x="0" y="-26">${order}</text>
      </svg>`,
    iconSize: [32, 48],
    iconAnchor: [16, 46],
    popupAnchor: [0, -44],
  })
}

function createTextElement(tagName, className, text) {
  const element = document.createElement(tagName)
  element.className = className
  element.textContent = text
  return element
}

function createPopupContent(stop) {
  const popup = document.createElement('article')
  popup.className = 'bread-popup'

  const head = document.createElement('div')
  head.className = 'bread-popup__head'
  head.appendChild(createTextElement('span', 'bread-popup__order', stop.order))
  head.appendChild(createTextElement('h3', 'bread-popup__name', stop.name))
  popup.appendChild(head)

  popup.appendChild(
    createTextElement('p', 'bread-popup__address', stop.address),
  )
  popup.appendChild(createTextElement('p', 'bread-popup__note', stop.note))

  return popup
}

function renderMarkers() {
  if (!map || !markerLayer) return

  markerLayer.clearLayers()
  markersByOrder = new Map()

  const bounds = []

  props.stops.forEach((stop) => {
    const marker = L.marker([stop.lat, stop.lng], {
      icon: createPinIcon(stop.order, stop.order === props.selectedOrder),
      title: `${stop.order}. ${stop.name}`,
      riseOnHover: true,
    })

    marker.bindPopup(createPopupContent(stop), {
      minWidth: 200,
      maxWidth: 260,
      autoPanPadding: [24, 24],
    })

    marker.on('click', () => {
      emit('select', stop.order)
    })

    // 팝업 ×/지도 빈 곳 클릭/Esc로 닫힐 때 선택 해제
    // (다른 핀 선택으로 닫힌 경우는 selectedOrder가 이미 바뀌어 있어 제외됨)
    marker.on('popupclose', () => {
      if (props.selectedOrder === stop.order) {
        emit('select', null)
      }
    })

    marker.addTo(markerLayer)
    markersByOrder.set(stop.order, marker)
    bounds.push([stop.lat, stop.lng])
  })

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 16 })
  }
}

onMounted(() => {
  map = L.map(mapContainer.value)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map)

  markerLayer = L.layerGroup().addTo(map)

  renderMarkers()
})

watch(() => props.stops, renderMarkers)

watch(
  () => props.selectedOrder,
  (order) => {
    if (!map) return

    markersByOrder.forEach((marker, markerOrder) => {
      const isSelected = markerOrder === order
      marker
        .getElement()
        ?.querySelector('.bread-pin')
        ?.classList.toggle('bread-pin--selected', isSelected)
      marker.setZIndexOffset(isSelected ? 1000 : 0)
    })

    if (order == null) {
      map.closePopup()
      return
    }

    markersByOrder.get(order)?.openPopup()
  },
)

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
    markerLayer = null
    markersByOrder = new Map()
  }
})
</script>

<template>
  <div class="course-map">
    <div
      ref="mapContainer"
      class="course-map__leaflet"
      aria-label="빵지순례 코스 지도"
    ></div>
  </div>
</template>

<style scoped>
.course-map__leaflet {
  width: 100%;
  height: 560px;
  min-height: 400px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  z-index: 0;
}

/* 핀 (divIcon 내부는 scoped 밖이므로 :deep 사용) */
.course-map :deep(.bread-pin-icon) {
  background: none;
  border: none;
  /* 아이콘 상자의 투명 영역이 아래 겹친 핀의 클릭을 가로채지 않도록
     실제 핀 모양(path/circle)에만 포인터 이벤트를 허용 */
  pointer-events: none !important;
}

.course-map :deep(.bread-pin__shape),
.course-map :deep(.bread-pin__badge) {
  pointer-events: auto;
}

.course-map :deep(.bread-pin) {
  overflow: visible;
  cursor: pointer;
  transform-box: fill-box;
  transform-origin: 50% 100%;
  transition: transform 0.15s ease;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.3));
}

.course-map :deep(.bread-pin:hover),
.course-map :deep(.leaflet-marker-icon:focus-visible .bread-pin) {
  transform: scale(1.15);
}

.course-map :deep(.bread-pin--selected) {
  transform: scale(1.2);
}

.course-map :deep(.bread-pin__shape) {
  fill: var(--color-primary);
  stroke: #fff;
  stroke-width: 1.5;
}

.course-map :deep(.leaflet-marker-icon:focus-visible .bread-pin__shape) {
  stroke: var(--color-accent);
  stroke-width: 3;
}

.course-map :deep(.bread-pin--selected .bread-pin__shape) {
  fill: var(--color-accent);
}

.course-map :deep(.bread-pin__badge) {
  fill: #fff;
}

.course-map :deep(.bread-pin__order) {
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 700;
  fill: var(--color-primary);
  text-anchor: middle;
  dominant-baseline: central;
  user-select: none;
  pointer-events: none;
}

/* 팝업(정보 카드) */
.course-map :deep(.leaflet-popup-content-wrapper) {
  border-radius: var(--radius-md);
}

.course-map :deep(.leaflet-popup-content) {
  margin: 14px 16px;
  font-family: var(--font-sans);
}

.course-map :deep(.bread-popup__head) {
  display: flex;
  align-items: center;
  gap: 8px;
}

.course-map :deep(.bread-popup__order) {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--color-accent);
  color: #fff;
  font-size: var(--font-size-caption);
  font-weight: 700;
}

.course-map :deep(.bread-popup__name) {
  margin: 0;
  font-size: var(--font-size-small);
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.4;
}

.course-map :deep(.bread-popup__address) {
  margin: 8px 0 0;
  font-size: var(--font-size-caption);
  color: var(--color-text-secondary);
}

.course-map :deep(.bread-popup__note) {
  margin: 4px 0 0;
  font-size: var(--font-size-caption);
  color: var(--color-text);
  line-height: 1.5;
}

@media (max-width: 820px) {
  .course-map__leaflet {
    height: 420px;
  }
}
</style>

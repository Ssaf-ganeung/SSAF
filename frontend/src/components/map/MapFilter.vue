<script setup>
import { PLACE_TYPES } from "../../constants/placeTypes";

defineProps({
  contentTypeId: {
    type: String,
    default: "",
  },
  region: {
    type: String,
    default: "",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:contentTypeId", "update:region"]);

const regions = ["대전", "세종", "충북", "충남", "기타"];

function updateContentType(event) {
  emit("update:contentTypeId", event.target.value);
}

function updateRegion(event) {
  emit("update:region", event.target.value);
}
</script>

<template>
  <form class="map-filter" @submit.prevent>
    <label class="map-filter__field">
      <span class="map-filter__label"> 장소 유형 </span>

      <select
        :value="contentTypeId"
        :disabled="disabled"
        class="map-filter__select"
        @change="updateContentType"
      >
        <option value="">전체</option>

        <option
          v-for="placeType in PLACE_TYPES"
          :key="placeType.id"
          :value="placeType.id"
        >
          {{ placeType.name }}
        </option>
      </select>
    </label>

    <label class="map-filter__field">
      <span class="map-filter__label"> 권역 </span>

      <select
        :value="region"
        :disabled="disabled"
        class="map-filter__select"
        @change="updateRegion"
      >
        <option value="">전체</option>

        <option
          v-for="regionOption in regions"
          :key="regionOption"
          :value="regionOption"
        >
          {{ regionOption }}
        </option>
      </select>
    </label>
  </form>
</template>

<style scoped>
.map-filter {
  display: flex;
  gap: 16px;
  padding: 16px;
  margin-bottom: 16px;
  background: rgba(117, 221, 221, 0.18);
  border: 1px solid #75dddd;
  border-radius: 10px;
}

.map-filter__field {
  display: flex;
  flex: 1;
  gap: 8px;
  align-items: center;
}

.map-filter__label {
  flex-shrink: 0;
  color: #172a3a;
  font-size: 14px;
  font-weight: 700;
}

.map-filter__select {
  width: 100%;
  min-width: 0;
  padding: 9px 12px;
  color: #172a3a;
  background: #fff;
  border: 1px solid #508991;
  border-radius: 7px;
}

.map-filter__select:focus {
  border-color: #09bc8a;
  outline: 2px solid rgba(9, 188, 138, 0.2);
}

.map-filter__select:disabled {
  cursor: wait;
  opacity: 0.6;
}

@media (max-width: 640px) {
  .map-filter {
    flex-direction: column;
  }
}
</style>

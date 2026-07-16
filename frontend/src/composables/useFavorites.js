import { computed, ref } from "vue";

const STORAGE_KEY = "ssaf.favorite-place-keys";

function createPlaceKey(place) {
  return `${place.content_type_id}:${place.id}`;
}

function loadFavoriteKeys() {
  try {
    const savedValue = localStorage.getItem(STORAGE_KEY);

    if (!savedValue) {
      return new Set();
    }

    const parsedValue = JSON.parse(savedValue);

    if (!Array.isArray(parsedValue)) {
      return new Set();
    }

    return new Set(parsedValue.filter((value) => typeof value === "string"));
  } catch (error) {
    console.error("즐겨찾기를 불러오지 못했습니다.", error);

    return new Set();
  }
}

const favoriteKeys = ref(loadFavoriteKeys());

export function useFavorites() {
  const favoriteCount = computed(() => favoriteKeys.value.size);

  function saveFavoriteKeys() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...favoriteKeys.value]));
  }

  function isFavorite(place) {
    return favoriteKeys.value.has(createPlaceKey(place));
  }

  function toggleFavorite(place) {
    const placeKey = createPlaceKey(place);
    const nextFavoriteKeys = new Set(favoriteKeys.value);

    if (nextFavoriteKeys.has(placeKey)) {
      nextFavoriteKeys.delete(placeKey);
    } else {
      nextFavoriteKeys.add(placeKey);
    }

    favoriteKeys.value = nextFavoriteKeys;
    saveFavoriteKeys();
  }

  return {
    favoriteCount,
    favoriteKeys,
    isFavorite,
    toggleFavorite,
  };
}

import accommodationMarker from "../assets/map-markers/accommodation.webp";
import attractionMarker from "../assets/map-markers/attraction.webp";
import courseMarker from "../assets/map-markers/course.webp";
import cultureMarker from "../assets/map-markers/culture.webp";
import defaultMarker from "../assets/map-markers/default.webp";
import festivalMarker from "../assets/map-markers/festival.webp";
import leisureMarker from "../assets/map-markers/leisure.webp";
import restaurantMarker from "../assets/map-markers/restaurant.webp";
import shoppingMarker from "../assets/map-markers/shopping.webp";

export const COLORS = {
  pearlAqua: "#75DDDD",
  pacificCyan: "#508991",
  deepSpaceBlue: "#172A3A",
  darkTeal: "#004346",
  mintLeaf: "#09BC8A",
};

const COMMON_ICON_OPTIONS = {
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -30],
};

export const PLACE_TYPES = [
  {
    id: "12",
    name: "관광지",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: attractionMarker,
    },
  },
  {
    id: "14",
    name: "문화시설",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: cultureMarker,
    },
  },
  {
    id: "15",
    name: "축제공연행사",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: festivalMarker,
    },
  },
  {
    id: "25",
    name: "여행코스",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: courseMarker,
    },
  },
  {
    id: "28",
    name: "레포츠",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: leisureMarker,
    },
  },
  {
    id: "32",
    name: "숙박",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: accommodationMarker,
    },
  },
  {
    id: "38",
    name: "쇼핑",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: shoppingMarker,
    },
  },
  {
    id: "39",
    name: "음식점",
    icon: {
      ...COMMON_ICON_OPTIONS,
      iconUrl: restaurantMarker,
    },
  },
];

export const PLACE_TYPE_MAP = Object.fromEntries(
  PLACE_TYPES.map((placeType) => [placeType.id, placeType]),
);

export const FALLBACK_ICON_OPTIONS = {
  ...COMMON_ICON_OPTIONS,
  iconUrl: defaultMarker,
};

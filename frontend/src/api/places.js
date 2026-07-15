import client from "./client";

export function getPlaces(params = {}) {
  return client.get("/api/places", {
    params,
  });
}

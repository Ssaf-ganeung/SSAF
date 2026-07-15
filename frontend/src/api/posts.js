import client from './client'
import { ALL_CATEGORY } from '../constants/postCategories'

export function fetchPosts({ category } = {}) {
  const params = category && category !== ALL_CATEGORY ? { category } : {}
  return client.get('/api/posts', { params })
}

export function fetchPost(id) {
  return client.get(`/api/posts/${id}`)
}

export function createPost(payload) {
  return client.post('/api/posts', payload)
}

export function updatePost(id, payload) {
  return client.put(`/api/posts/${id}`, payload)
}

export function deletePost(id, payload) {
  return client.delete(`/api/posts/${id}`, { data: payload })
}

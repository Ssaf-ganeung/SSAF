import client from './client'

// TODO: 백엔드 게시글 CRUD 라우터 구현 후 엔드포인트 연동

export function fetchPosts() {
  return client.get('/api/posts')
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

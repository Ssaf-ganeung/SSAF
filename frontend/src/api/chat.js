import client from './client'

// TODO: 백엔드 POST /api/chat 구현 후 연동

export function sendChatMessage(message) {
  return client.post('/api/chat', { message })
}

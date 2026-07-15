import client from './client'

// 대화 히스토리 전체(messages 배열)를 백엔드로 전송한다.
// messages: [{ role: 'user' | 'assistant', content: string }, ...]
export function sendChatMessage(messages) {
  return client.post('/api/chat', { messages })
}

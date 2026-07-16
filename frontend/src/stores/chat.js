import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    isOpen: false,
    isLoading: false, // 답변 생성 대기 중 여부
    messages: [], // { role: 'user' | 'assistant', content: string }
  }),
  actions: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    addMessage(role, content) {
      this.messages.push({ role, content })
    },
    setLoading(value) {
      this.isLoading = value
    },
  },
})

import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    isOpen: false,
    messages: [], // { role: 'user' | 'assistant', content: string }
  }),
  actions: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    addMessage(role, content) {
      this.messages.push({ role, content })
    },
  },
})

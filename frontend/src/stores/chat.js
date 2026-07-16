import { defineStore } from "pinia";

export const useChatStore = defineStore("chat", {
  state: () => ({
    isOpen: false,
    isLoading: false, // 답변 생성 대기 중 여부
    messages: [], // { role: 'user' | 'assistant', content: string }
  }),
  actions: {
    toggle() {
      this.isOpen = !this.isOpen;
    },
    addMessage(role, content, relatedPlaces = [], relatedPosts = []) {
      this.messages.push({
        role,
        content,
        relatedPlaces,
        relatedPosts,
      });
    },
    setLoading(value) {
      this.isLoading = value;
    },
    appendToLastAssistantMessage(content) {
      const lastMessage = this.messages[this.messages.length - 1];

      if (lastMessage?.role === "assistant") {
        lastMessage.content += content;
      }
    },

    setLastAssistantRelatedPlaces(relatedPlaces) {
      const lastMessage = this.messages[this.messages.length - 1];

      if (lastMessage?.role === "assistant") {
        lastMessage.relatedPlaces = relatedPlaces;
      }
    },

    setLastAssistantRelatedPosts(relatedPosts) {
      const lastMessage = this.messages[this.messages.length - 1];

      if (lastMessage?.role === "assistant") {
        lastMessage.relatedPosts = relatedPosts;
      }
    },
  },
});

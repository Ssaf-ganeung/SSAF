import client from "./client";

// 대화 히스토리 전체(messages 배열)를 백엔드로 전송한다.
// messages: [{ role: 'user' | 'assistant', content: string }, ...]
export function sendChatMessage(messages) {
  return client.post("/api/chat", { messages });
}

export async function streamChatMessage(messages, handlers) {
  const baseUrl = import.meta.env.VITE_API_BASE_URL ?? "";

  const response = await fetch(`${baseUrl}/api/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ messages }),
  });

  if (!response.ok) {
    throw new Error(`Chat stream failed: ${response.status}`);
  }

  if (!response.body) {
    throw new Error("스트리밍 응답 본문이 없습니다.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();

    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });

    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";

    for (const eventText of events) {
      const lines = eventText.split("\n");

      const eventLine = lines.find((line) => line.startsWith("event:"));
      const dataLine = lines.find((line) => line.startsWith("data:"));

      if (!eventLine || !dataLine) {
        continue;
      }

      const eventName = eventLine.slice(6).trim();
      const data = JSON.parse(dataLine.slice(5).trim());

      if (eventName === "places") {
        handlers.onPlaces?.(data);
      }

      if (eventName === "posts") {
        handlers.onPosts?.(data);
      }

      if (eventName === "delta") {
        handlers.onDelta?.(data.content);
      }

      if (eventName === "done") {
        handlers.onDone?.();
      }
    }
  }
}

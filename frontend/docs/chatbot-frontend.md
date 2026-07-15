# 챗봇 기능 설계 문서 — 프론트엔드

작업 브랜치: `feature/chatbot`

> 기능 개요·요구사항 매핑은 루트 [`docs/chatbot.md`](../../docs/chatbot.md) 참고. 백엔드 설계는 [`backend/docs/chatbot-backend.md`](../../backend/docs/chatbot-backend.md) 참고.

## 1. 구성

우하단 플로팅 위젯으로 어느 화면에서나 접근 가능한 챗봇. 대화 히스토리는 Pinia store에 보관하여 페이지를 이동해도 유지된다(익명이므로 로그인 없이 브라우저 세션 단위로 유지).

## 2. 컴포넌트

| 컴포넌트 | 역할 |
|---|---|
| `ChatWidget.vue` | 플로팅 버튼 + 패널 토글, 전송 처리(로딩/에러 핸들링), 헤더·닫기 |
| `ChatWindow.vue` | 대화 히스토리 렌더링(스크롤 영역), 자동 스크롤, "입력 중…" 표시, 빈 상태 안내 |
| `ChatMessage.vue` | 개별 말풍선(user 오른쪽/assistant 왼쪽), 줄바꿈 유지 |
| `ChatInput.vue` | 입력창 + 전송 버튼, 로딩 중 비활성화 |

## 3. 상태 관리 (`stores/chat.js`)

| state | 설명 |
|---|---|
| `isOpen` | 패널 열림/닫힘 |
| `isLoading` | 답변 생성 대기 여부(입력 잠금·타이핑 표시에 사용) |
| `messages` | `{ role, content }` 배열(대화 히스토리) |

- actions: `toggle()`, `addMessage(role, content)`, `setLoading(value)`

## 4. 전송 흐름

```
ChatInput(submit) →emit send→ ChatWidget.handleSend
  ① store.addMessage('user', text)          # 내 메시지 표시
  ② store.setLoading(true)                   # 입력 잠금 + 타이핑 표시
  ③ sendChatMessage(store.messages)          # 대화 전체를 POST /api/chat
  ④ store.addMessage('assistant', reply)     # 답변 표시
  ⑤ 실패 시 catch → ⚠️ 안내 메시지 표시
  ⑥ finally → setLoading(false)
```

- `api/chat.js`의 `sendChatMessage(messages)`가 `{ messages }`를 백엔드로 전송.

## 5. UX 처리

- **로딩**: `isLoading` 동안 "대·충 봇이 입력 중…" 표시 + 입력/버튼 비활성화.
- **에러**: 요청 실패 시 대화창에 안내 문구 노출(앱이 멈추지 않음).
- **자동 스크롤**: 메시지 추가·로딩 변화 시 `nextTick` 후 맨 아래로 스크롤.
- **모바일**: 화면 폭 480px 이하에서 패널을 전체 화면으로 확장.

## 6. 파일 트리 (구현 대상)

```
frontend/
└── src/
    ├── api/chat.js                       # 수정: { message } → { messages } 전송
    ├── stores/chat.js                    # 수정: isLoading 상태 + setLoading 추가
    └── components/chat/
        ├── ChatWidget.vue                # 수정: 로딩/에러 처리, 헤더·닫기, 스타일
        ├── ChatWindow.vue                # 수정: 자동 스크롤, 타이핑/빈 상태 표시
        ├── ChatMessage.vue               # 수정: 말풍선 스타일
        └── ChatInput.vue                 # 수정: 로딩 중 비활성화
```

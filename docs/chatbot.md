# 챗봇 기능 설계 문서

작업 브랜치: `feature/chatbot`

## 1. 개요

제공된 대전·충청권 관광 JSON 데이터(1,365건)를 근거로 자연어 지역 정보 질의응답을 처리하는 AI 챗봇. 우하단 플로팅 위젯으로 어느 화면에서나 접근할 수 있으며, 관광지 추천·축제 일정·맛집 위치 등 주요 질의에 응답한다. OpenAI를 호출하되 질문과 관련된 실제 장소를 검색해 프롬프트에 근거로 주입하는 **RAG(검색 증강 생성)** 방식으로 환각을 억제한다. 익명 서비스이므로 로그인 없이 대화 히스토리는 브라우저(Pinia)에 세션 단위로 유지한다.

## 2. 기능 명세

### 2.1 REST API (`/api/chat`)

| Method | Path | 설명 | 요청 바디 | 응답 |
|---|---|---|---|---|
| POST | `/api/chat` | 대화 히스토리를 받아 답변 생성 | `{ messages: [{ role, content }, ...] }` | `{ reply }` |
| GET | `/api/chat/search` | [디버그] OpenAI 없이 키워드 검색 결과만 반환 | 쿼리 `?q=...&limit=8` | 장소 배열 |

- 서버는 상태를 저장하지 않으며(stateless), 대화 맥락은 요청마다 프론트가 `messages` 배열 전체로 전달한다.
- RAG 검색은 가장 최근 사용자 메시지 기준. 최근 12개 메시지만 OpenAI에 전달(토큰/비용 제한).
- 키 미설정·호출 실패는 500이 아닌 안내 문구를 `reply`로 반환하여 대화창이 깨지지 않게 한다.

### 2.2 데이터 그라운딩 (RAG)

- 서버 시작 시 `data/대전_충청권_*.json`을 메모리에 로드·캐시.
- 1,365건 규모라 벡터DB·임베딩 없이 **키워드 매칭**으로 검색(장소명·지역명·유형 힌트·토큰 겹침 점수화).
- 검색된 실제 장소만 근거로 답하도록 시스템 프롬프트에 명시("목록에 없는 장소는 지어내지 마세요").

### 2.3 프론트엔드 화면

| 컴포넌트 | 역할 |
|---|---|
| `ChatWidget.vue` | 플로팅 버튼 + 패널 토글, 전송/로딩/에러 처리 |
| `ChatWindow.vue` | 대화 렌더링, 자동 스크롤, "입력 중…"·빈 상태 표시 |
| `ChatMessage.vue` | 말풍선(user 오른쪽/assistant 왼쪽) |
| `ChatInput.vue` | 입력창 + 전송, 로딩 중 비활성화 |

- 대화 히스토리·열림 상태·로딩 상태는 `stores/chat.js`(Pinia)에서 관리.
- UX: 로딩 표시, 에러 안내, 자동 스크롤, 모바일 전체화면(≤480px).

## 3. 파일 트리 (구현 대상)

```
backend/
└── app/
    ├── main.py                 # 수정: chat 라우터 include
    ├── core/config.py          # 수정: OPENAI_MODEL 설정 추가
    ├── schemas/chat.py         # 신규: ChatMessage / ChatRequest / ChatResponse
    ├── services/
    │   ├── chat_service.py     # 신규: OpenAI 호출 + 프롬프트/히스토리 구성
    │   └── place_data.py       # 신규: JSON 로딩 + 키워드 검색 + 포맷
    └── routers/chat.py         # 신규: POST /api/chat + GET /api/chat/search

frontend/
└── src/
    ├── api/chat.js             # 수정: { message } → { messages }
    ├── stores/chat.js          # 수정: isLoading 상태 추가
    └── components/chat/        # 수정: Widget/Window/Message/Input UX 개선

docs/
└── chatbot.md                  # 본 문서
```

## 4. 요구사항 ↔ 구현 매핑

| 요구사항 | 반영 방식 |
|---|---|
| 가. `POST /api/chat`(OpenAI) + 제공 JSON 기반 질의응답 | `routers/chat.py` + `chat_service.py`에서 OpenAI 호출, `place_data.py`로 JSON 검색해 근거 주입(RAG) |
| 나. 주요 질의 유형(관광지 추천·축제 일정·맛집 위치 등) 응답 | 유형 힌트 매핑(맛집→음식점, 축제→축제공연행사 등) + 지역명 필터로 관련 장소 검색 |
| 다. 대화 히스토리 유지·모바일 대응·플로팅 UI | Pinia store에 히스토리 보관, 요청마다 전체 전송, 플로팅 위젯 + 480px 이하 전체화면 |

## 5. 향후 미확정 사항

- 커뮤니티 게시글 검색 질의(`posts` 테이블 조회) 연동 — 커뮤니티 기능과 협업 필요, 후순위.
- 키워드 검색 매칭 규칙 고도화(동의어·형태소) 필요 여부.
- 스트리밍 응답(타이핑 효과) 적용 여부.
- 대화 히스토리의 새로고침 유지(localStorage) 적용 여부.

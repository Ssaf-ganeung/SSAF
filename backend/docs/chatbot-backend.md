# 챗봇 기능 설계 문서 — 백엔드

작업 브랜치: `feature/chatbot`

> 기능 개요·요구사항 매핑은 루트 [`docs/chatbot.md`](../../docs/chatbot.md) 참고. 프론트엔드 설계는 [`frontend/docs/chatbot-frontend.md`](../../frontend/docs/chatbot-frontend.md) 참고.

## 1. 개요

제공된 대전·충청권 관광 JSON(1,365건)을 근거로 자연어 질의응답을 처리하는 챗봇. OpenAI를 호출하되, 질문과 관련된 실제 장소를 검색해 프롬프트에 근거로 주입하는 **RAG(검색 증강 생성)** 방식으로 환각을 억제한다. 서버는 대화 상태를 저장하지 않으며(stateless), 대화 히스토리는 요청마다 프론트가 전체를 실어 보낸다.

## 2. REST API (`/api/chat`)

| Method | Path | 설명 | 요청 바디 | 응답 |
|---|---|---|---|---|
| POST | `/api/chat` | 대화 히스토리를 받아 답변 생성 | `{ messages: [{ role, content }, ...] }` | `{ reply }` |
| GET | `/api/chat/search` | [디버그] OpenAI 없이 키워드 검색 결과만 반환 | 쿼리 `?q=...&limit=8` | 장소 배열 |

- `messages`는 프론트 Pinia store와 동일한 `{ role: 'user'|'assistant', content }` 배열.
- RAG 검색은 **가장 최근 사용자 메시지** 기준으로 수행한다.
- 최근 `MAX_HISTORY`(=12)개 메시지만 OpenAI에 전달해 토큰/비용을 제한한다.
- `OPENAI_API_KEY` 미설정 시 500 대신 안내 문구를 `reply`로 반환(대화창이 깨지지 않도록).
- 호출 실패(네트워크/쿼터 등)도 안내 문구로 graceful 처리.

## 3. 데이터 그라운딩 (RAG)

- 서버 시작 후 최초 1회 `data/대전_충청권_*.json`을 메모리에 로드·캐시(`place_data.load_places`).
- 데이터가 1,365건뿐이라 **벡터DB·임베딩 없이 단순 키워드 매칭**으로 검색.
- 점수화: 장소명이 질문에 직접 등장(+5), 지역명이 주소와 일치(+2), 유형 힌트 일치(+2, 예 "맛집"→음식점), 일반 토큰 겹침(+1). 상위 N개를 프롬프트에 첨부.
- 시스템 프롬프트에 "목록에 없는 장소는 지어내지 마세요" 지시로 환각 억제.

## 4. 환경 변수 (`.env`)

| 키 | 기본값 | 설명 |
|---|---|---|
| `OPENAI_API_KEY` | `""` | OpenAI API 키. **커밋 금지**(`.gitignore` 등록) |
| `OPENAI_MODEL` | `gpt-4o-mini` | 사용할 모델명 |

## 5. 파일 트리 (구현 대상)

```
backend/
└── app/
    ├── main.py                 # 수정: chat 라우터 include
    ├── core/config.py          # 수정: OPENAI_MODEL 설정 추가
    ├── schemas/
    │   └── chat.py             # 신규: ChatMessage / ChatRequest / ChatResponse
    ├── services/
    │   ├── chat_service.py     # 신규: OpenAI 호출 + 히스토리/프롬프트 구성(generate_reply)
    │   └── place_data.py       # 신규: JSON 로딩 + 키워드 검색(search_places) + 포맷(format_context)
    └── routers/
        └── chat.py             # 신규: APIRouter, POST /api/chat + GET /api/chat/search
```

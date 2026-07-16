# 프로젝트 진행 현황

## Branch

feature/chatbot

## 목표

OpenAI 기반 지역 정보 챗봇 구현

---

## 완료

- [x] 챗봇 기능 요구사항 분석
- [x] ChatWidget 구조 설계

### Backend

- [x] OpenAI API 연동 (`chat_service.py`, 모델은 `.env`의 `OPENAI_MODEL`)
- [x] JSON Loader (`place_data.py` — 1,365건 로딩·메모리 캐시)
- [x] Prompt 작성 (SYSTEM_PROMPT + RAG 근거 주입, 환각 억제 지시)
- [x] 지역 데이터 키워드 검색 (RAG, 벡터DB 없이 경량 매칭)
- [x] POST /api/chat (대화 히스토리 배열 수신 → 답변)
- [x] 대화 히스토리 멀티턴 처리 (최근 12개 컨텍스트 유지)
- [x] GET /api/chat/search (디버그용 검색 엔드포인트)
- [x] POST /api/chat/stream (SSE 기반 답변 스트리밍)
- [x] 추천 결과와 지도 링크 검색 결과 일치
- [x] 직전 추천 장소를 이용한 후속 질문 검색
- [x] 좌표 기반 주변 장소 직선거리 검색

### Frontend

- [x] ChatWidget (플로팅 버튼 + 패널, 전송/로딩/에러 처리)
- [x] ChatWindow (자동 스크롤, 입력 중 표시, 빈 상태 안내)
- [x] ChatMessage (말풍선 UI)
- [x] ChatInput (로딩 중 비활성화)
- [x] Pinia Store 연동 (히스토리·열림·로딩 상태)
- [x] UX 마감 (로딩·에러·자동스크롤·모바일 전체화면)
- [x] 관련 장소 지도 링크 및 후속 검색용 장소 ID 전달

### 문서

- [x] 설계 문서 3종 (`docs/chatbot.md`, `backend/docs/chatbot-backend.md`, `frontend/docs/chatbot-frontend.md`)

---

## 진행 중

- [ ] 프론트 챗봇 UI 브라우저 실사용 검증 (로딩/에러/스크롤 눈으로 확인)
- [ ] feature/chatbot → main PR 병합

---

## 차단

없음 (키 모델 권한 이슈는 `gpt-5-mini`로 해결)

---

## 결정 완료

- [x] Prompt 정책 — RAG(관련 장소 검색 후 프롬프트에 근거 주입) + "목록에 없는 장소는 지어내지 않기"
- [x] 응답 포맷 — `{ reply, related_places }` 및 SSE 이벤트
- [x] Context 관리 방식 — 프론트가 `messages` 배열 전체 전송(stateless), 서버는 최근 12개만 사용

---

## 다음 작업

1. 프론트 UI 실사용 검증
2. PR 올려 main 병합
3. (선택) 커뮤니티 게시글 검색 질의 연동 — 커뮤니티 기능과 협업, 후순위
4. (배포 단계) Render 환경변수에 `OPENAI_API_KEY`, `OPENAI_MODEL` 설정

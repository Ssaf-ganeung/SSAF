# 프로젝트 진행 현황

## Branch

feature/community-crud

## 목표

익명 커뮤니티 CRUD 구현

---

## 완료

- [x] 익명 커뮤니티 방식 확정
- [x] 게시글 비밀번호 평문 저장 정책 확정
- [x] 커뮤니티 CRUD API 설계
- [x] Post 데이터 모델 설계

---

## 진행 중

### Backend

- [ ] Post Model
- [ ] Schema
- [ ] CRUD
- [ ] Router
- [ ] SQLite 연동
- [ ] GET /api/posts
- [ ] GET /api/posts/{id}
- [ ] POST /api/posts
- [ ] PUT /api/posts/{id}
- [ ] DELETE /api/posts/{id}

### Frontend

- [ ] PostListView
- [ ] PostDetailView
- [ ] PostFormView
- [ ] PasswordConfirmModal
- [ ] Axios 연동

---

## 차단

없음

---

## 결정 대기

- [ ] 페이지네이션 적용 여부
- [ ] 제목 길이 제한
- [ ] 내용 길이 제한
- [ ] 비밀번호 길이 제한

---

## 다음 작업

1. SQLAlchemy Post 모델
2. CRUD 작성
3. Router 작성
4. Vue CRUD 화면 구현
5. API 연동

---

## 진행 기록 규칙

- API 완료 시 체크
- UI 완료 시 체크

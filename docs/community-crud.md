# 커뮤니티 CRUD 설계 문서

작업 브랜치: `feature/community-crud`

## 1. 개요

별도의 회원가입·로그인 없이 누구나 글을 쓸 수 있는 익명 커뮤니티 게시판을 구현한다. 인증/권한 체계는 적용하지 않으며, 글 작성 시 함께 등록한 비밀번호로만 수정·삭제 권한을 확인한다. 선정한 1개 권역(지자체 권역)을 대상으로 하는 단일 카테고리 게시판이므로, 이번 MVP에서는 DB에 별도의 `category`/`region` 컬럼을 두지 않고 게시판 자체를 해당 권역 전용으로 취급한다. (다중 권역/카테고리로 확장이 필요해지면 `Post`에 `category` 컬럼을 추가하는 방향으로 확장 가능)

## 2. 기능 명세

### 2.1 데이터 모델 (`Post`)

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | Integer (PK) | 자동 증가 |
| `title` | String | 제목, 필수 |
| `content` | Text | 내용, 필수 |
| `password` | String | 수정/삭제용 비밀번호. **평문 저장·평문 비교** (해시 없음 — 교육 목적의 의도된 설계) |
| `created_at` | DateTime | 작성일시, 서버에서 자동 설정 |
| `updated_at` | DateTime | 수정일시, 수정 시 자동 갱신 |

### 2.2 REST API (`/api/posts`)

| Method | Path | 설명 | 요청 바디 | 비고 |
|---|---|---|---|---|
| GET | `/api/posts` | 목록 조회 | - | `created_at` 내림차순 정렬, `password` 제외한 필드만 응답 |
| GET | `/api/posts/{id}` | 상세 조회 | - | 없는 id는 404 |
| POST | `/api/posts` | 작성 | `{ title, content, password }` | 3개 필드 모두 필수 |
| PUT | `/api/posts/{id}` | 수정 | `{ title, content, password }` | `password`가 저장된 값과 일치할 때만 반영, 불일치 시 403 |
| DELETE | `/api/posts/{id}` | 삭제 | `{ password }` | 일치할 때만 삭제, 불일치 시 403 |

- 응답 스키마(`PostResponse`)는 `password` 필드를 절대 포함하지 않는다.
- 비밀번호 검증은 `저장된 값 == 요청 값` 문자열 비교로만 수행한다. 해시/암호화를 적용하지 않는다.
- 존재하지 않는 게시글에 대한 조회/수정/삭제는 404, 비밀번호 불일치는 403으로 응답한다.

### 2.3 프론트엔드 화면

| 라우트 | 컴포넌트 | 설명 |
|---|---|---|
| `/community` | `PostListView.vue` | 목록 조회, `PostCard.vue` 반복 렌더링 |
| `/community/new` | `PostFormView.vue` | 작성 폼 (`PostForm.vue` 재사용) |
| `/community/:id` | `PostDetailView.vue` | 상세 조회, 수정/삭제 진입점 |
| `/community/:id/edit` | `PostFormView.vue` | 수정 폼 (`PostForm.vue` 재사용, 기존 값 프리필) |

- 수정/삭제 시 `PasswordConfirmModal.vue`로 비밀번호를 입력받아 API 요청에 실어 보낸다.
- 비밀번호 불일치(403) 시 모달에 에러 메시지를 표시하고 재입력을 받는다.

## 3. 파일 트리 (구현 대상)

```
backend/
└── app/
    ├── main.py                 # 수정: Base.metadata.create_all 호출 + post 라우터 include
    ├── models/
    │   └── post.py             # 신규: SQLAlchemy Post 모델
    ├── schemas/
    │   └── post.py             # 신규: PostCreate / PostUpdate / PostDelete / PostResponse
    ├── crud/
    │   └── post.py             # 신규: get_posts / get_post / create_post / update_post / delete_post
    └── routers/
        └── post.py             # 신규: APIRouter, /api/posts 엔드포인트 5종

frontend/
└── src/
    ├── api/posts.js            # 기존 파일 — 엔드포인트 시그니처 확정(이미 구현되어 있음)
    ├── router/index.js         # 기존 파일 — 라우트 그대로 사용(이미 구현되어 있음)
    ├── views/community/
    │   ├── PostListView.vue    # 구현: fetchPosts 연동 + 목록 렌더링
    │   ├── PostDetailView.vue  # 구현: fetchPost 연동 + 수정/삭제 진입점
    │   └── PostFormView.vue    # 구현: id 유무로 작성/수정 모드 분기
    └── components/community/
        ├── PostCard.vue                # 구현: 목록 카드(제목/날짜 등)
        ├── PostForm.vue                # 구현: 제목/내용/비밀번호 입력 + 유효성 검사
        └── PasswordConfirmModal.vue    # 구현: 비밀번호 입력 모달 + 에러 표시

docs/
└── community-crud.md           # 본 문서
```

## 4. 요구사항 ↔ 구현 매핑

| 요구사항 | 반영 방식 |
|---|---|
| 가. 인증 없는 익명 커뮤니티 | 백엔드에 인증 미들웨어/의존성을 두지 않음, 프론트엔드에 로그인 화면·상태 없음 |
| 나. 작성 시 비밀번호 등록, 평문 저장·비교로만 권한 확인 | `Post.password`를 평문 `String` 컬럼으로 저장, 수정/삭제 요청의 `password`와 `==` 비교하여 일치 여부만으로 권한 판단 |
| 다. 선정 권역 카테고리 게시판의 목록/상세/작성/수정/삭제 API + Vue 화면 | 위 2.2/2.3의 `/api/posts` 라우터와 `views/community` · `components/community` |
| 라. 커뮤니티 데이터의 DB 저장·관리 | SQLAlchemy `Post` 모델 + SQLite(`app.db`), 앱 시작 시 `Base.metadata.create_all(bind=engine)` 호출로 테이블 생성 |

## 5. 향후 미확정 사항

- 목록 API 페이지네이션 적용 여부
- `PostForm.vue` 클라이언트 측 유효성 검사 규칙 (제목/내용 길이 제한 등)
- 실제 대상 권역명 확정 및 README 등 상위 문서 반영

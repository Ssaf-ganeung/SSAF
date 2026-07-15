# 커뮤니티 CRUD 설계 문서 — 백엔드

작업 브랜치: `feature/community-crud`

> 기능 개요·요구사항 매핑·향후 미확정 사항은 루트 [`architecture.md`](../../architecture.md#커뮤니티-crud-기능) 참고. 프론트엔드 설계는 [`frontend/docs/community-crud-frontend.md`](../../frontend/docs/community-crud-frontend.md) 참고.

## 1. 데이터 모델 (`Post`)

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | Integer (PK) | 자동 증가 |
| `title` | String | 제목, 필수 |
| `content` | Text | 내용, 필수 |
| `password` | String | 수정/삭제용 비밀번호. **평문 저장·평문 비교** (해시 없음 — 교육 목적의 의도된 설계) |
| `created_at` | DateTime | 작성일시, 서버에서 자동 설정 |
| `updated_at` | DateTime | 수정일시, 수정 시 자동 갱신 |

## 2. REST API (`/api/posts`)

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
```

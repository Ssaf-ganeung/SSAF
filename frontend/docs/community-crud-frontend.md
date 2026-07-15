# 커뮤니티 CRUD 설계 문서 — 프론트엔드

작업 브랜치: `feature/community-crud`

> 기능 개요·요구사항 매핑·향후 미확정 사항은 루트 [`architecture.md`](../../architecture.md#커뮤니티-crud-기능) 참고. 백엔드 설계는 [`backend/docs/community-crud-backend.md`](../../backend/docs/community-crud-backend.md) 참고.

## 1. 화면 구성

| 라우트 | 컴포넌트 | 설명 |
|---|---|---|
| `/community` | `PostListView.vue` | 목록 조회, `PostCard.vue` 반복 렌더링 |
| `/community/new` | `PostFormView.vue` | 작성 폼 (`PostForm.vue` 재사용) |
| `/community/:id` | `PostDetailView.vue` | 상세 조회, 수정/삭제 진입점 |
| `/community/:id/edit` | `PostFormView.vue` | 수정 폼 (`PostForm.vue` 재사용, 기존 값 프리필) |

- 수정/삭제 시 `PasswordConfirmModal.vue`로 비밀번호를 입력받아 API 요청에 실어 보낸다.
- 비밀번호 불일치(403) 시 모달에 에러 메시지를 표시하고 재입력을 받는다.

## 2. 파일 트리 (구현 대상)

```
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
```

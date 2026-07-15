# Backend Constraints

이 문서의 규칙은 백엔드 구현 시 반드시 지켜야 하는 HARD 제약이다.

## 1. 런타임 및 의존성

- Python 가상환경은 `backend/venv`를 사용한다.
- 패키지 의존성은 `backend/requirements.txt`에서 관리한다.
- Poetry, Pipenv, uv 등 다른 의존성 관리 도구를 임의로 추가하지 않는다.
- 데이터베이스는 현재 SQLite를 사용한다.
- 배포 전까지 PostgreSQL 등 다른 DB로 변경하지 않는다.

## 2. 환경 변수

- 실제 `.env` 파일은 Git에 커밋하지 않는다.
- 공유 가능한 키 이름과 예시는 `.env.example`에만 작성한다.
- OpenAI API 키를 코드, 문서, 테스트 데이터에 하드코딩하지 않는다.
- 기본 DB URL은 `sqlite:///./app.db`를 사용한다.

## 3. 레이어 책임

- ORM 모델은 `app/models`에 둔다.
- 요청·응답 스키마는 `app/schemas`에 둔다.
- DB 처리 함수는 `app/crud`에 둔다.
- HTTP 라우팅은 `app/routers`에 둔다.
- 라우터에 복잡한 DB 로직을 직접 작성하지 않는다.
- 라우터는 `get_db()` 의존성을 통해 세션을 주입받는다.

## 4. 커뮤니티 인증 및 권한

- 회원가입 기능을 추가하지 않는다.
- 로그인 기능을 추가하지 않는다.
- JWT, 세션, OAuth 인증을 추가하지 않는다.
- 게시글 수정·삭제 권한은 작성 비밀번호 일치 여부만으로 판단한다.
- 비밀번호가 일치하지 않으면 `403 Forbidden`을 반환한다.
- 존재하지 않는 게시글은 비밀번호 검증 전에 `404 Not Found`를 반환한다.

## 5. 비밀번호 처리

현재 요구사항은 교육 목적의 의도된 설계다.

- `Post.password`는 평문 `String` 컬럼으로 저장한다.
- 요청 비밀번호와 저장 비밀번호를 `==` 문자열 비교한다.
- 별도 합의 없이 해시, 암호화, salt를 적용하지 않는다.
- 게시글 응답 스키마에는 `password` 필드를 정의하지 않는다.
- 로그와 예외 메시지에 비밀번호를 출력하지 않는다.

> 실제 운영 서비스에서는 반드시 비밀번호 해시를 적용해야 한다.

## 6. Post 모델

현재 MVP의 필수 컬럼:

- `id`
- `title`
- `content`
- `password`
- `created_at`
- `updated_at`

다음 컬럼은 현재 추가하지 않는다.

- `user_id`
- `author_id`
- `category`
- `region`
- `deleted_at`

다중 권역 또는 회원 기능이 확정된 이후 별도 설계로 추가한다.

## 7. API 계약

기본 prefix:

```text
/api/posts
```

필수 엔드포인트:

- `GET /api/posts`
- `GET /api/posts/{id}`
- `POST /api/posts`
- `PUT /api/posts/{id}`
- `DELETE /api/posts/{id}`

필수 상태 코드:

- 정상 조회·수정: `200`
- 정상 생성: `201`
- 정상 삭제: `204` 또는 팀 합의된 단일 응답 형식
- 게시글 없음: `404`
- 비밀번호 불일치: `403`
- 요청 검증 실패: `422`

목록 응답은 `created_at` 내림차순이어야 한다.

## 8. 데이터베이스 초기화

현재 초기 단계에서는 앱 시작 시 다음 방식을 사용한다.

```python
Base.metadata.create_all(bind=engine)
```

Alembic은 이후 DB 마이그레이션 필요성이 확정되기 전까지 추가하지 않는다.

## 9. CORS

- 허용 origin은 `CORS_ORIGINS` 환경 변수에서 읽는다.
- 기본 개발 origin은 `http://localhost:5173`이다.
- 개발 편의를 이유로 무조건 `*`를 사용하지 않는다.

## 10. 범위 밖 작업

현재 단계에서 다음 작업은 수행하지 않는다.

- 공공데이터의 SQLite 적재 및 변경 API
- OpenAI 챗봇 로직 구현
- 배포 설정 파일 생성
- Git 저장소 초기화 및 원격 연결
- 사용자 인증 기능
- 페이지네이션
- CSS 프레임워크 도입

지도 시각화 기능에서는 `backend/data/`의 공공데이터 JSON을
읽기 전용으로 조회하는 API를 제공할 수 있다.

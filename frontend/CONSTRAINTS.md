# Frontend Constraints

이 문서의 규칙은 프론트엔드 구현 시 반드시 지켜야 하는 HARD 제약이다.

## 1. 언어 및 도구

- Vue 3 Composition API 기반으로 작성한다.
- TypeScript를 사용하지 않는다.
- `.ts`, `.tsx` 파일을 추가하지 않는다.
- 프론트엔드 코드는 `frontend/` 내부에서 독립 관리한다.
- 루트에 통합 `package.json`을 생성하지 않는다.

## 2. 필수 의존성

다음 패키지를 사용한다.

- `vue-router`
- `pinia`
- `axios`

CSS 프레임워크는 결정 전까지 설치하지 않는다.

임의로 다음 도구를 추가하지 않는다.

- Tailwind CSS
- Bootstrap
- Vuetify
- PrimeVue
- Pinia 외 다른 전역 상태 라이브러리

## 3. 라우팅

다음 라우트를 유지한다.

- `/`
- `/community`
- `/community/new`
- `/community/:id`
- `/community/:id/edit`

작성과 수정 화면을 별도 파일로 중복 구현하지 않는다.

`PostFormView.vue`와 `PostForm.vue`를 작성·수정에 공용으로 사용한다.

## 4. 인증

- 로그인 화면을 만들지 않는다.
- 회원가입 화면을 만들지 않는다.
- 사용자 인증 상태 store를 만들지 않는다.
- JWT를 저장하거나 전송하는 로직을 추가하지 않는다.
- 게시글 수정·삭제 시 작성 비밀번호만 입력받는다.

## 5. 비밀번호

- 비밀번호 입력값을 브라우저 저장소에 저장하지 않는다.
- `localStorage`, `sessionStorage`, cookie에 게시글 비밀번호를 저장하지 않는다.
- 비밀번호를 URL query 또는 path parameter에 포함하지 않는다.
- 수정·삭제 API 요청 body에만 포함한다.
- 화면에 서버에 저장된 비밀번호를 표시하지 않는다.

## 6. API 호출

- Axios 인스턴스는 `src/api/client.js`에서만 생성한다.
- API base URL을 컴포넌트에 하드코딩하지 않는다.
- `VITE_API_BASE_URL` 환경 변수를 사용한다.
- 게시글 API 함수는 `src/api/posts.js`에 모은다.
- 챗봇 API 함수는 `src/api/chat.js`에 모은다.
- View 또는 컴포넌트에서 Axios URL 문자열을 반복 작성하지 않는다.

## 7. 상태 관리

Pinia는 플로팅 챗봇 상태 유지에 사용한다.

필수 상태:

- `isOpen`
- `messages`

초기 MVP에서 게시글 CRUD 데이터를 Pinia 전역 store로 이동하지 않는다.

## 8. 컴포넌트 책임

- View는 데이터 요청과 페이지 단위 상태를 담당한다.
- 재사용 가능한 UI는 `components/`에 둔다.
- `PostForm.vue`는 입력 UI와 submit event 전달에 집중한다.
- `PostCard.vue`는 목록의 단일 게시글 표현을 담당한다.
- `PasswordConfirmModal.vue`는 비밀번호 입력과 확인·취소 이벤트만 담당한다.
- 챗봇 메시지 렌더링과 입력을 하나의 대형 컴포넌트에 모두 작성하지 않는다.

## 9. 초기 세팅 범위

초기 스캐폴딩 단계에서는 다음만 작성한다.

- 최소 template/script/style 골격
- 컴포넌트 이름
- props 및 emit 예정 위치
- TODO 주석
- 기본 라우트 연결
- Pinia 초기 상태
- Axios 기본 인스턴스

다음은 기능 구현 단계까지 작성하지 않는다.

- 실제 CRUD 요청 처리
- 실제 챗봇 요청 처리
- 복잡한 폼 검증
- 디자인 시스템
- CSS 프레임워크
- 배포 설정

## 10. 응답 및 오류 처리

- `403` 응답은 비밀번호 불일치 안내로 처리한다.
- `404` 응답은 게시글 없음 안내로 처리한다.
- API 오류를 성공 상태처럼 처리하지 않는다.
- 서버가 반환하지 않은 `password` 값을 응답 객체에 가정하여 사용하지 않는다.

## 11. 범위 밖 작업

현재 단계에서 다음 작업은 수행하지 않는다.

- Netlify 설정 파일 생성
- Git 초기화 및 remote 연결
- 관리자 화면
- 다중 권역 필터
- 게시글 카테고리
- 댓글 기능
- 사용자 프로필

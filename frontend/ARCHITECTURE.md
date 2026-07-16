# Frontend Architecture

## 1. 역할

프론트엔드는 Vue 3 기반 SPA로 다음 기능을 제공한다.

- 지역 정보 서비스 홈 화면
- 익명 커뮤니티 목록·상세·작성·수정 화면
- 게시글 삭제 및 수정 전 비밀번호 확인
- 페이지 이동과 무관하게 상태가 유지되는 플로팅 AI 챗봇
- FastAPI REST API 연동

## 2. 기술 스택

- Vue.js 3
- Vite
- JavaScript
- Vue Router
- Pinia
- Axios
- Leaflet

TypeScript와 CSS 프레임워크(Tailwind 등)는 사용하지 않는다. 디자인 토큰은 `src/style.css`의 순수 CSS 커스텀 프로퍼티로 관리한다.

## 3. 디렉터리 구조

```text
frontend/
├── ARCHITECTURE.md
├── CONSTRAINTS.md
├── docs/
│   └── community-crud-frontend.md
├── index.html
├── vite.config.js
├── package.json
├── .env.example
└── src/
    ├── main.js
    ├── App.vue
    ├── router/
    │   └── index.js
    ├── stores/
    │   └── chat.js
    ├── views/
    │   ├── HomeView.vue
    │   ├── MapView.vue
    │   └── community/
    │       ├── PostListView.vue
    │       ├── PostDetailView.vue
    │       └── PostFormView.vue
    ├── components/
    │   ├── common/
    │   │   ├── AppHeader.vue
    │   │   ├── AppFooter.vue
    │   │   ├── BaseButton.vue
    │   │   └── Pagination.vue
    │   ├── community/
    │   │   ├── PostCard.vue
    │   │   ├── PostForm.vue
    │   │   └── PasswordConfirmModal.vue
    │   ├── chat/
    │   │   ├── ChatWidget.vue
    │   │   ├── ChatWindow.vue
    │   │   ├── ChatMessage.vue
    │   │   └── ChatInput.vue
    │   └── map/
    │       ├── LeafletMap.vue
    │       ├── MapFilter.vue
    │       └── PlaceDetailPanel.vue
    ├── api/
    │   ├── client.js
    │   ├── posts.js
    │   ├── chat.js
    │   └── places.js
    ├── constants/
    │   └── placeTypes.js
    └── assets/
        └── map-markers/
            └── *.webp
```

## 4. 애플리케이션 진입점

### `src/main.js`

다음을 등록한다.

- Vue 앱
- Vue Router
- Pinia
- 전역 CSS

### `src/App.vue`

공통 레이아웃을 담당한다.

기본 배치:

```text
AppHeader
RouterView
AppFooter
ChatWidget
```

`ChatWidget`은 특정 화면 내부가 아니라 `App.vue`에 배치하여 모든 라우트에서 유지한다.

## 5. 라우팅

필수 라우트:

| Path                  | View                 | 설명        |
| --------------------- | -------------------- | ----------- |
| `/`                   | `HomeView.vue`       | 홈          |
| `/map`                | `MapView.vue`        | 지역 지도   |
| `/community`          | `PostListView.vue`   | 게시글 목록 |
| `/community/new`      | `PostFormView.vue`   | 게시글 작성 |
| `/community/:id`      | `PostDetailView.vue` | 게시글 상세 |
| `/community/:id/edit` | `PostFormView.vue`   | 게시글 수정 |

작성과 수정은 동일한 `PostFormView.vue` 및 `PostForm.vue`를 재사용한다.

## 6. 상태 관리

### `stores/chat.js`

Pinia를 사용하여 플로팅 챗봇 상태를 관리한다.

관리 대상:

- `isOpen`: 챗봇 패널 열림 여부
- `messages`: 사용자와 AI의 대화 내역

커뮤니티 화면 이동 시에도 챗봇 상태와 메시지가 유지되어야 한다.

게시글 CRUD 상태는 초기 MVP에서 각 View의 로컬 상태로 관리하고, 전역 store를 추가하지 않는다.

## 7. API 레이어

### `api/client.js`

Axios 인스턴스를 생성한다.

```text
baseURL = import.meta.env.VITE_API_BASE_URL
```

### `api/posts.js`

게시글 API 호출 함수를 정의한다.

- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 작성
- 게시글 수정
- 게시글 삭제

컴포넌트에서 Axios URL을 직접 반복 작성하지 않는다.

### `api/chat.js`

향후 `POST /api/chat` 호출 함수를 정의한다.

### `api/places.js`

`GET /api/places`를 호출하고 다음 선택 필터를 쿼리 파라미터로 전달한다.

- `content_type_id`: TourAPI 8개 콘텐츠 유형 ID
- `region`: 대전·세종·충북·충남·기타

## 8. 지도 화면 구성

### 데이터 흐름

```text
MapFilter
→ MapView 필터 상태
→ api/places.js
→ GET /api/places
→ LeafletMap places props
→ WebP Marker / Popup
→ select-place event
→ PlaceDetailPanel
```

### `MapView.vue`

페이지 단위 상태와 API 요청을 담당한다.

- 장소 목록
- 선택한 콘텐츠 유형과 권역
- 로딩·오류·빈 결과 상태
- 필터 변경 시 장소 API 재요청
- 연속 요청의 응답 순서가 뒤바뀌지 않도록 요청 sequence 관리
- Marker에서 전달받은 선택 장소 상태 관리
- 필터 결과에서 선택 장소가 제외되면 상세 패널 닫기

### `MapFilter.vue`

- 전체 및 8개 콘텐츠 유형 선택
- 전체 및 권역 선택
- 로딩 중 입력 비활성화
- 선택값을 `v-model` 이벤트로 `MapView`에 전달

### `LeafletMap.vue`

- OpenStreetMap Tile Layer 렌더링
- `places` props 변경 감시
- LayerGroup을 사용한 기존 Marker 제거 및 재생성
- 장소 전체 범위에 `fitBounds()` 적용
- 컴포넌트 해제 시 Leaflet map 인스턴스 정리
- Marker 클릭 Popup 렌더링
- Marker 클릭 시 `select-place` 이벤트 전달

Popup 문자열은 HTML 문자열 결합 대신 DOM `textContent`를 사용한다. 이미지 로딩에 실패하면 이미지 요소만 제거한다.

### `PlaceDetailPanel.vue`

선택한 장소의 확장 정보를 표시한다.

- 데스크톱에서는 지도 우측 패널, 좁은 화면에서는 지도 아래 패널로 배치
- 대표 이미지와 이미지 누락 상태 표시
- 콘텐츠 유형, 장소명, 주소, 전화번호, 권역 표시
- 전화번호가 있으면 `tel:` 링크 제공
- 카카오맵 위치 보기 및 길찾기 URL 제공
- 닫기 이벤트를 `MapView`에 전달

### Marker 리소스

`constants/placeTypes.js`에서 콘텐츠 유형과 WebP Marker 이미지를 연결한다.

```text
12 관광지
14 문화시설
15 축제공연행사
25 여행코스
28 레포츠
32 숙박
38 쇼핑
39 음식점
```

Marker 원본은 `src/assets/map-markers/`에서 관리하고 화면에서는 `32x32` 크기로 표시한다.

## 9. 커뮤니티 화면 구성

### `PostListView.vue`

- 게시글 목록 요청
- 작성 페이지 이동 버튼
- `PostCard` 반복 렌더링
- 로딩·오류·빈 목록 상태 표시

### `PostDetailView.vue`

- 게시글 상세 요청
- 수정 화면 진입
- 삭제 버튼
- 삭제 시 `PasswordConfirmModal` 표시

### `PostFormView.vue`

라우트에 따라 작성과 수정을 구분한다.

- `/community/new`: 작성 모드
- `/community/:id/edit`: 수정 모드

수정 모드에서는 게시글 상세를 먼저 조회해 제목과 내용을 채운다.

### `PostForm.vue`

입력 필드:

- 제목
- 내용
- 비밀번호

제출 이벤트는 부모 View에 전달한다.

### `PasswordConfirmModal.vue`

수정 또는 삭제 권한 확인용 비밀번호 입력 UI다.

현재 구체적인 UX는 추후 구현 단계에서 결정한다.

## 10. 챗봇 컴포넌트 구성

- `ChatWidget.vue`: 플로팅 버튼과 패널 토글
- `ChatWindow.vue`: 전체 대화 렌더링 및 스크롤 영역
- `ChatMessage.vue`: user/assistant 메시지 말풍선
- `ChatInput.vue`: 입력창과 전송 버튼

초기 세팅 단계에서는 UI 골격과 TODO만 작성한다.

## 11. 환경 변수

`.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Vite에서 클라이언트 코드가 접근할 환경 변수는 반드시 `VITE_` 접두사를 사용한다.

## 12. 초기 실행 검증

```bash
cd frontend
npm install
npm run dev
```

확인 주소:

```text
http://localhost:5173
```

확인 항목:

- 기본 화면 렌더링
- 각 커뮤니티 라우트 접근
- `/map` 지도, Marker, Popup 렌더링
- 콘텐츠 유형 및 권역 필터 동작
- 새로고침 시 라우터 오류 여부
- ChatWidget 공통 노출 여부

## 13. 향후 확장

- 실제 게시글 CRUD API 연동
- 챗봇 API 연동
- 폼 유효성 검사
- 공통 로딩·오류 컴포넌트
- Marker clustering 및 지도 렌더링 성능 개선
- CSS 프레임워크 적용
- 반응형 디자인
- Netlify 배포 설정

`components/common/`(AppHeader, AppFooter, BaseButton, Pagination)의 디자인 토큰 적용은 완료됨. `components/community/`, `components/chat/` 등 나머지 컴포넌트는 아직 토큰을 적용하지 않았다(챗봇 컴포넌트는 `#2f6fed`를 여전히 하드코딩 중).

# 프로젝트 진행 현황

## Branch

feature/map-visualization

## 목표

`backend/data/`의 TourAPI 4.0 공공데이터를 조회 API로 제공하고,
Leaflet 지도에 TourAPI 공공데이터 8개 유형을 Marker 및 Popup으로 시각화한다.

## 데이터 흐름

```text
backend/data JSON
→ FastAPI 장소 조회 API
→ Axios 장소 API 함수
→ MapView
→ LeafletMap
→ Marker / Popup / Filter
```

---

## 완료

- [x] 지도 시각화 기능 선정
- [x] 공공데이터 JSON 파일 확보
- [x] 공공데이터 필드 구조 문서화 (`backend/data/SCHEMA.md`)
- [x] 공공데이터 출처 문서화 (`backend/data/SOURCE.md`)

---

## 구현 체크리스트

### 1. 범위와 API 계약 결정

- [x] 지도 표시 대상을 공공데이터 8개 유형 전체로 확정
- [ ] 지도 공급자를 Leaflet + OpenStreetMap으로 확정
- [x] 콘텐츠 유형 필터 값 결정 (`12`, `14`, `15`, `25`, `28`, `32`, `38`, `39`)
- [x] 권역 필터 범위 결정 (대전/세종/충북/충남/기타, 주소 기준)
- [ ] `GET /api/places` 요청 및 응답 형식 문서화
- [x] `backend/CONSTRAINTS.md`의 공공데이터 범위와 현재 작업 범위 충돌 정리

### 2. 공공데이터 확인 및 정규화

- [x] 8개 JSON의 최상위 구조와 `items` 배열 검증
- [x] 전체 1,365개 원본 항목을 `TourApiDataset`으로 검증
- [x] `contentid`를 장소 ID로 사용하도록 원본 스키마 정의
- [x] `contenttypeid` 8개 유형을 `ContentTypeId`로 정의
- [x] `mapx` 문자열을 경도 `float`로 변환
- [x] `mapy` 문자열을 위도 `float`로 변환
- [x] 좌표가 비어 있거나 숫자로 변환되지 않는 항목 제외
- [x] `addr1`, `addr2`를 화면 표시용 주소로 정리
- [x] `firstimage`가 빈 문자열인 경우 이미지 없음으로 처리
- [x] `title`, `tel`, `firstimage` 등 Popup 응답 필드 정의
- [x] 주소를 기준으로 권역을 구분하는 규칙 작성

### 3. Backend 장소 조회 API

- [x] `app/schemas/place.py` 생성
- [x] `TourApiItem`, `TourApiDataset` 원본 스키마 정의
- [x] `PlaceResponse` 응답 스키마 정의
- [x] `app/services/place_service.py` 생성
- [x] 실행 위치에 영향받지 않는 JSON 파일 경로 처리
- [x] JSON 파일 읽기 함수 작성
- [x] 원본 항목을 `PlaceResponse` 형태로 변환하는 함수 작성
- [x] 8개 JSON 데이터를 하나의 장소 목록으로 결합
- [x] 콘텐츠 유형 필터 구현
- [x] 권역 필터 구현
- [ ] `app/routers/place.py` 생성
- [ ] `GET /api/places` 엔드포인트 구현
- [ ] `app/main.py`에 장소 라우터 등록
- [ ] Swagger에서 전체 장소 조회 확인
- [ ] Swagger에서 8개 콘텐츠 유형 필터 확인
- [ ] Swagger에서 권역 필터 확인
- [ ] 응답의 위도·경도가 숫자 타입인지 확인

### 4. Frontend Leaflet 기본 설정

- [ ] `frontend` 의존성 설치 (`npm install`)
- [ ] Leaflet 설치 (`npm install leaflet`)
- [ ] Leaflet CSS import
- [ ] 지도 컨테이너 너비와 높이 지정
- [ ] OpenStreetMap Tile Layer 설정
- [ ] 지도 초기 중심 좌표와 zoom 결정
- [ ] 빈 지도 렌더링 확인
- [ ] 컴포넌트 해제 시 Leaflet map 인스턴스 정리

### 5. Frontend 장소 API 연동

- [ ] `src/api/places.js` 생성
- [ ] 기존 Axios client를 사용해 `GET /api/places` 호출
- [ ] `src/views/MapView.vue` 생성
- [ ] 장소 목록 상태 작성
- [ ] 로딩 상태 작성
- [ ] 오류 상태 작성
- [ ] API 응답을 `LeafletMap`에 props로 전달
- [ ] 브라우저 Network에서 API 요청 성공 확인

### 6. 지도 컴포넌트와 Marker

- [ ] `src/components/map/LeafletMap.vue` 생성
- [ ] `places` props 정의
- [ ] Marker를 관리할 Leaflet LayerGroup 생성
- [ ] 8개 콘텐츠 유형 Marker 출력
- [ ] 콘텐츠 유형별 Marker 구분 방식 적용
- [ ] 장소 목록 변경 시 기존 Marker 제거 후 다시 출력
- [ ] Marker 결과가 있을 때 `fitBounds()` 적용
- [ ] Marker가 없을 때 `fitBounds()`가 호출되지 않도록 처리
- [ ] Marker 한 개일 때 최대 확대 수준 제한

### 7. Popup

- [ ] Marker 클릭 시 Popup 표시
- [ ] Popup에 장소명 표시
- [ ] Popup에 장소 유형 표시
- [ ] Popup에 주소 표시
- [ ] 전화번호가 있을 때만 표시
- [ ] 대표 이미지가 있을 때만 표시
- [ ] 이미지가 없어도 레이아웃이 깨지지 않는지 확인
- [ ] 공공데이터 문자열을 Popup HTML에 안전하게 표시

### 8. Filter

- [ ] `src/components/map/MapFilter.vue` 생성
- [ ] 전체/8개 콘텐츠 유형 필터 UI 작성
- [ ] 권역 필터 UI 작성
- [ ] 유형 필터 변경 시 API 재요청
- [ ] 권역 필터 변경 시 API 재요청
- [ ] 유형과 권역 조합 필터 확인
- [ ] 조회 결과가 없을 때 빈 결과 안내 표시
- [ ] 필터 변경 후 Marker가 중복되지 않는지 확인

### 9. Router 및 화면 연결

- [ ] `/map` 라우트 추가
- [ ] 기존 필수 라우트가 유지되는지 확인
- [ ] `AppHeader.vue`에 지도 이동 링크 추가
- [ ] 직접 `/map` 접근 시 화면 렌더링 확인
- [ ] 다른 화면 이동 후 다시 돌아왔을 때 지도 재생성 확인

### 10. 최종 검증 및 문서화

- [ ] Backend 실행 확인
- [ ] Frontend 실행 확인
- [ ] 8개 콘텐츠 유형 Marker 표시 확인
- [ ] Popup 동작 확인
- [ ] 유형 Filter 동작 확인
- [ ] 권역 Filter 동작 확인
- [ ] 좌표·이미지·주소 누락 데이터 예외 처리 확인
- [ ] 브라우저 콘솔 오류가 없는지 확인
- [ ] Frontend 빌드 확인 (`npm run build`)
- [ ] `backend/ARCHITECTURE.md`에 장소 API 구조 반영
- [ ] `frontend/ARCHITECTURE.md`에 지도 화면 구조 반영
- [ ] `branches/map/PROGRESS.md` 완료 항목 갱신

---

## 결정 대기

- [ ] 권역 Filter의 정확한 구분 기준
- [ ] 8개 콘텐츠 유형 Marker 디자인
- [ ] Popup 상세 UI

---

## 차단

없음

---

## 다음 작업

1. API 문서를 8개 콘텐츠 유형 기준으로 수정
2. `app/routers/place.py` 작성
3. `app/main.py`에 장소 라우터 등록
4. `/api/places`의 전체·유형·권역 필터 검증
5. Swagger에서 장소 API 확인

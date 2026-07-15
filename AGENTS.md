# SSAF 프로젝트 작업 가이드

## 1. 프로젝트 개요

지자체 권역 공공데이터를 기반으로 지역 정보를 제공하는 웹 서비스다.

주요 기능은 다음과 같다.

- 선정 권역의 지역 정보 제공
- 로그인 없는 익명 커뮤니티
- 작성 비밀번호 기반 게시글 수정·삭제
- OpenAI 기반 플로팅 AI 챗봇

현재 저장소는 `backend/`와 `frontend/`가 독립적으로 구성된 모노레포 구조를 사용한다.

## 2. 확정 기술 스택

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- pydantic-settings
- OpenAI API
- 가상환경: `venv`
- 의존성 관리: `requirements.txt`

### Frontend

- Vue.js 3
- Vite
- JavaScript
- Vue Router
- Pinia
- Axios

### Deployment

- Frontend: Netlify 예정
- Backend: Render 예정
- 배포 설정 파일은 이후 별도 작업에서 추가한다.

## 3. 저장소 구조

```text
ssaf/
├── AGENTS.md
├── PROGRESS.md
├── Makefile
├── .gitignore
├── README.md
├── architecture.md
├── backend/
│   ├── ARCHITECTURE.md
│   ├── CONSTRAINTS.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── data/
│   └── app/
└── frontend/
    ├── ARCHITECTURE.md
    ├── CONSTRAINTS.md
    ├── package.json
    ├── vite.config.js
    ├── .env.example
    └── src/
```

## 4. 실행 명령어

루트 `Makefile`을 기준으로 실행한다.

```bash
make setup
make dev-backend
make dev-frontend
make check
```

백엔드만 직접 실행하는 경우:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell에서는 다음 명령으로 가상환경을 활성화한다.

```powershell
.\venv\Scripts\Activate.ps1
```

프론트엔드만 직접 실행하는 경우:

```bash
cd frontend
npm install
npm run dev
```

## 5. 전역 HARD 제약

다음 규칙은 별도 합의 없이 변경하지 않는다.

1. 루트 통합 `package.json`을 만들지 않는다.
2. `backend/`와 `frontend/`는 독립 실행 구조를 유지한다.
3. 프론트엔드는 TypeScript가 아닌 JavaScript를 사용한다.
4. CSS 프레임워크는 결정 전까지 설치하지 않는다.
5. 백엔드는 `venv + requirements.txt` 구조를 유지한다.
6. 데이터베이스는 현재 SQLite를 사용한다.
7. 커뮤니티에는 회원가입·로그인·인증 미들웨어를 추가하지 않는다.
8. 게시글 수정·삭제 권한은 작성 시 등록한 비밀번호로만 확인한다.
9. 현재 교육용 요구사항에 따라 게시글 비밀번호는 평문 저장·평문 비교한다.
10. API 응답에 게시글 비밀번호를 절대 포함하지 않는다.
11. 단일 권역 전용 게시판이므로 현재 `category`, `region` 컬럼을 추가하지 않는다.
12. 배포 설정 파일과 Git 연결 작업은 별도 단계에서 진행한다.

세부 제약은 다음 문서를 따른다.

- Backend: [`backend/CONSTRAINTS.md`](backend/CONSTRAINTS.md)
- Frontend: [`frontend/CONSTRAINTS.md`](frontend/CONSTRAINTS.md)

## 6. 현재 구현 범위

### 초기 세팅

- 로컬 폴더 및 파일 스캐폴딩
- FastAPI 기본 앱, CORS, health check
- SQLAlchemy DB 연결 구조
- Vue Router, Pinia, Axios 기반 SPA 골격
- 커뮤니티와 챗봇 컴포넌트 최소 골격

### 커뮤니티 CRUD

작업 브랜치:

```text
feature/community-crud
```

구현 대상:

- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 작성
- 게시글 수정
- 게시글 삭제
- 수정·삭제 시 비밀번호 검증

## 7. 작업 시 문서 우선순위

충돌이 발생하면 다음 순서로 판단한다.

1. `backend/CONSTRAINTS.md`, `frontend/CONSTRAINTS.md`
2. `AGENTS.md`
3. 각 영역의 `ARCHITECTURE.md`
4. `PROGRESS.md`
5. 코드 내 TODO 및 주석

구현 중 제약이나 설계 결정을 변경해야 한다면 코드만 수정하지 말고 관련 문서도 함께 수정한다.

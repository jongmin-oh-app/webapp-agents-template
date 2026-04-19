# Web App Monorepo (TDD)

## Architecture Overview

```
webapp-agents-template/
├── apps/
│   ├── web/              # React + Vite + TypeScript (Frontend)
│   │   ├── src/__tests__/ # Vitest 유닛/통합 테스트
│   │   └── e2e/           # Playwright E2E 테스트
│   └── api/              # Python FastAPI + Mangum (AWS Lambda)
│       └── tests/         # pytest 유닛/통합 테스트
├── supabase/
│   ├── migrations/       # DB 마이그레이션
│   └── seed.sql          # 시드 데이터
└── .github/workflows/    # CI/CD
```

- `apps/web`과 `apps/api`는 완전히 독립된 프로젝트 (언어가 다르므로 코드 공유 없음)
- API 타입 공유: Backend Pydantic → OpenAPI 스펙 → `apps/web/src/types/api.ts` 자동 생성

## Tech Stack
- **Frontend**: React 19, Vite, TypeScript, TanStack Query, React Router
- **Frontend Test**: Vitest, React Testing Library, MSW
- **Backend**: Python 3.12, FastAPI, Mangum, Pydantic
- **Backend Test**: pytest, httpx
- **E2E Test**: Playwright
- **Infra**: AWS Lambda Function URL, ECR, SAM
- **Database/Auth**: Supabase (PostgreSQL, Auth, Storage)

## TDD Workflow (필수 준수)

모든 기능 개발은 반드시 아래 순서를 따른다:

```
Phase 1: 설계        Architect → API 스키마, 기능 명세
                      Backend → DB 설계 (Supabase 스키마, RLS, 마이그레이션)
                      Reviewer → DB 스키마 검증
    ↓
Phase 2: 테스트 (Red) Tester → E2E 테스트 선행 작성
                      Frontend → Vitest 유닛 테스트 선행 작성
                      Backend → pytest 유닛 테스트 선행 작성
    ↓
Phase 3: 구현 (Green) Frontend → 테스트 통과하는 최소 구현
                      Backend → 테스트 통과하는 최소 구현
    ↓
Phase 4: 검증        Frontend/Backend → 리팩토링 (Refactor)
                      Tester → E2E 전체 실행, 회귀 테스트
                      Reviewer → TDD 준수 + 코드 품질 리뷰
```

## Agent Team Roles
- **Architect** (Opus): 설계 + 인프라 총괄 — API 스키마, AWS/Supabase 인프라, CI/CD, TDD 워크플로우 조율
- **Frontend** (Sonnet): `apps/web/` — Vitest 테스트 선행 작성 → React 구현
- **Backend** (Sonnet): `apps/api/` + `supabase/` — DB 설계 + pytest 테스트 선행 작성 → FastAPI 구현
- **Tester** (Sonnet): `apps/web/e2e/` — Playwright E2E 테스트 선행 작성 + 회귀 검증
- **Reviewer** (Opus): 읽기 전용 — TDD 준수 검증 + 코드 품질/보안 리뷰

## Conventions
- API 엔드포인트: `/api/v1/` 접두사
- 환경변수: `.env.example`에 키 목록 관리, 시크릿은 코드에 포함 금지
- Supabase 스키마 변경: 반드시 마이그레이션 파일로 관리
- Frontend에서 Backend 호출: Lambda Function URL 직접 호출
- **테스트 없는 구현 코드 작성 금지**
- Frontend 컴포넌트: 반드시 `data-testid` 속성 부여

## Code Conventions (모든 에이전트 필수 준수)

### 1. 간결함이 최우선
- 코드는 최대한 짧고 간결하게 작성한다
- 3줄로 될 것을 10줄로 쓰지 않는다
- 불필요한 추상화, 헬퍼, 유틸리티 함수를 만들지 않는다
- 한 번만 쓰는 로직은 인라인으로 작성한다

### 2. 죽은 코드 즉시 삭제
- 사용하지 않는 코드는 발견 즉시 삭제한다
- "나중에 쓸지도 모르는" 코드는 무조건 삭제한다 — 필요하면 그때 다시 작성한다
- 주석 처리된 코드(`// old logic`, `# TODO: maybe later`)는 남기지 않는다
- 사용하지 않는 import, 변수, 함수, 컴포넌트는 즉시 제거한다

### 3. 레거시 금지
- 하위 호환용 코드, 폐기 예정(deprecated) 래퍼는 만들지 않는다
- 기존 코드가 불필요해지면 바로 삭제하고 새 코드로 교체한다
- `_unused`, `legacy_`, `old_` 같은 접두사로 코드를 보존하지 않는다

### 4. 주석은 최소한으로
- 코드로 의도가 드러나면 주석을 달지 않는다
- 주석은 "왜(Why)"만 적는다 — "무엇(What)"은 코드 자체가 설명한다
- JSDoc, docstring은 외부 공개 API에만 작성한다
- `// increment counter`, `# get user` 같은 자명한 주석은 금지

### 5. 예외처리 최소화
- 개발 단계에서는 예외처리를 하지 않는다 — 에러가 그대로 터져야 디버깅이 쉽다
- try-catch/try-except는 **외부 시스템 경계**(API 호출, DB 연결)에서만 사용한다
- 내부 로직에서 방어적 코딩(null 체크, 타입 가드 남발)을 하지 않는다
- "혹시 모를" 예외처리는 금지 — 실제로 발생하는 에러만 처리한다

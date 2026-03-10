---
name: sveltekit-progressive-architecture
description: "SvelteKit 프로젝트 아키텍처·코드 규칙. Actions: 작성, 구현, 리뷰, 리팩터, 검토, 추가, 설계, 수정, write, implement, review, refactor, fix. Base Rules: 컴포넌트 재사용, $lib, 라우트 배치, 인라인 타입 금지, interface, type, script 섹션, 주석, 가독성, code style, TypeScript. Server Architecture: 서버 아키텍처, Active Record, Query Service, REST API, Drizzle, +server.ts, +page.server.ts, server/domain, server/infra, 뷰모델, view-model, form actions, ORM, schema, 레이어 분리, CUD, load."
allowed-tools: Bash Read Write Edit
metadata:
  author: dev-goraebap
---

# SvelteKit Progressive Architecture

SvelteKit 프로젝트에 적용하는 아키텍처와 코드 작성 규칙.

## 언제 적용하나

- SvelteKit 코드를 작성하거나 리뷰할 때
- 서버 레이어 설계 또는 API 엔드포인트를 구현할 때
- 코드 스타일·타입 정의·파일 구조를 결정할 때

## 카테고리

| 카테고리 | 적용 상황 | 참조 파일 |
|----------|-----------|-----------|
| **Base Rules** | `.svelte` 파일 작성, 타입 정의, `$lib` 구조, 주석 | [base-rules.md](references/base-rules.md) |
| **Server Architecture** | `+server.ts`, `+page.server.ts`, domain/infra 레이어, Drizzle, REST API | [server-architecture.md](references/server-architecture.md) |

## 핵심 규칙 요약

### Base Rules

- **라우트 우선 배치**: 반복 패턴이 보여도 `$lib`로 바로 빼지 않는다
- **`$lib/components`는 신중하게**: 3개 이상 페이지에서 쓰이는 범용 UI만
- **인라인 타입 금지**: 반드시 `interface`나 `type`으로 분리 정의
- **스크립트 섹션 주석**: `<script>` 영역은 역할별로 섹션 주석

### Server Architecture

- **레이어 분리**: `server/domain/` (Active Record CUD) + `server/infra/` (Query Service 조회)
- **직접 ORM 조작 금지**: `+server.ts` → Domain Model, `+page.server.ts` → Query Service
- **R/CUD 분리**: load는 `+page.server.ts`, 쓰기는 `routes/api/` REST 엔드포인트
- **form actions 미사용**: REST API로 분리하여 백엔드 이식성 확보
- **서버 타입이 원천**: 조회 뷰모델은 `infra/view-models/`에 정의

## 실행 방법

### Step 1: 작업 분류

요청 내용을 보고 해당하는 카테고리를 파악한다. 여러 카테고리에 걸치는 경우 모두 포함한다.

| 요청 예시 | 카테고리 |
|-----------|----------|
| `.svelte` 파일 작성, 타입 정의, `$lib` 구조 | Base Rules |
| `+server.ts`, `+page.server.ts`, DB 쿼리, REST API | Server Architecture |
| 전체 코드 리뷰 | 모두 |

### Step 2: 참조 파일 로드

카테고리 테이블에서 해당 참조 파일을 읽는다. 상세 규칙과 코드 예시가 포함되어 있다.

### Step 3: 규칙 적용

참조 파일의 규칙에 따라 코드를 작성하거나 리뷰한다. 규칙에 어긋나는 부분이 있으면 지적하고 수정 방향을 제안한다.

## 자율 실행 원칙

**확인 없이 즉시 수행:**
- 코드 파일 읽기·작성·수정
- 새 파일·디렉토리 생성
- 패키지 의존성 확인 (`package.json` 읽기)

**사용자에게 먼저 물어볼 것:**
- 기존 파일 삭제가 필요한 경우
- 아키텍처 방향이 명확히 불명확한 경우

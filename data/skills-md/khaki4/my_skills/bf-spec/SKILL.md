---
name: bf-spec
description: AC 문서를 입력받아 Tech Spec을 작성하고, 자동으로 bf-lead-review를 통해 다관점 리뷰를 수행한다. BF 워크플로우 진입점.
---

# BF Spec (Entry Point)

## Overview

BF 워크플로우의 진입점이다. 기획자가 제공한 AC 문서를 기반으로 Tech Spec을 작성하고, 자동으로 `bf-lead-review`를 스폰하여 다관점 리뷰를 수행한다. 리뷰 결과를 사람에게 제시하여 승인 여부를 판단하게 한다 (사람 개입 ①).

## When to Use

- 사용자가 `/bf-spec`을 입력했을 때
- 새로운 기능 개발 또는 변경 요청이 있을 때

## Prerequisites

- 워크플로우 진입점이므로 별도 전제조건 없음
- 사용자가 AC 문서 또는 변경 요청 내용을 준비한 상태여야 함

## Error Handling

- AC 문서가 제공되지 않으면: "AC 문서 또는 변경 요청 내용을 제공해 주세요." 안내
- Jira 티켓 번호 미제공 시: "Jira 티켓 번호를 알려주세요. 없으면 임시 ID를 생성합니다." 안내 후 `BF-{YYYYMMDD}-{N}` 형식으로 자동 생성
- bf-lead-review 스폰 실패 시: 메인 세션에서 단일 Opus로 리뷰를 직접 수행하고, 사용자에게 "Agent Teams 구성에 실패하여 단독으로 리뷰합니다."를 알림

## Instructions

### 1. 입력 수집

사용자에게 다음 입력을 요청한다:
- AC 문서 또는 내용
- 관련 Jira 티켓 번호

### 2. 코드베이스 분석 및 초기 conventions.md 생성

기존 코드베이스를 분석한다:
- 변경 대상 모듈/파일 식별
- 기존 아키텍처 패턴 확인
- 의존성 그래프 파악

**conventions.md 초기 생성** (`docs/conventions.md`가 없는 경우):
- 코드베이스 분석 결과를 기반으로 초기 conventions.md를 생성한다:
  ```markdown
  # 프로젝트 컨벤션

  ## 아키텍처
  - {프레임워크}: {발견된 아키텍처 패턴 — 예: Layered, Hexagonal}
  - 모듈 구조: {발견된 디렉토리/모듈 규칙}

  ## 네이밍
  - 파일명: {발견된 패턴 — 예: kebab-case, PascalCase}
  - 함수/변수: {발견된 패턴}

  ## 테스트
  - 테스트 프레임워크: {발견된 도구}
  - 테스트 파일 위치: {규칙}

  ## 코드 스타일
  - {발견된 주요 코드 스타일 규칙}

  {아래 concern-area 섹션은 코드베이스에서 해당 기술 스택이 감지된 경우에만 포함}

  ## UI 패턴
  - {React/Vue/Angular 등 감지 시: 컴포넌트 구조, 상태 관리 패턴}

  ## API 패턴
  - {Express/Fastify/NestJS/Django 등 감지 시: 엔드포인트 설계, 에러 핸들링 패턴}

  ## DB 패턴
  - {Prisma/TypeORM/Drizzle 등 감지 시: 스키마 규칙, 마이그레이션 패턴}
  ```
- concern-area 섹션(UI Patterns, API Patterns, Database Patterns, Security Patterns, Infrastructure Patterns)은 코드베이스에서 해당 기술 스택이 감지된 경우에만 포함한다. 감지되지 않은 기술 스택의 섹션은 생성하지 않는다. 초기 seed이므로 핵심 패턴만 간결하게 기재하고, 이후 `/bf-update-conventions`가 축적한다.
- 이미 존재하면 건너뛴다.

### 3. Tech Spec 작성

아래 템플릿에 따라 Tech Spec 문서를 작성한다:

```markdown
# {TICKET} Tech Spec

## 배경
{변경 목적, 비즈니스 배경, 사용자 문제}

## 현재 상태 (As-Is)
{현재 아키텍처, 관련 모듈 구조, 데이터 흐름}
{코드베이스 분석 결과 반영}

## 목표 상태 (To-Be)
{변경 후 아키텍처, 모듈 구조, 데이터 흐름}
{주요 설계 결정 및 근거}

## 영향 분석
- 변경 대상 파일/모듈: {목록}
- 의존성 영향: {상위/하위 모듈 영향}
- 사이드이펙트: {예상되는 부작용}
- 하위 호환성: {호환성 유지 여부 및 전략}

## 인수 조건
{기획자 AC 그대로 포함}
- [ ] AC 1: {구체적이고 테스트 가능한 기준}
- [ ] AC 2: ...

## 기술 제약
- {성능 요구사항}
- {보안 고려사항}
- {기존 기술 스택 제약}
- {인프라/배포 제약}

## 테스트 전략
- 단위 테스트: {범위 및 접근}
- E2E 테스트: {시나리오 개요}
- 엣지 케이스: {예상 엣지 케이스 목록}

## 리스크
| 리스크 | 영향도 | 완화 전략 |
|--------|--------|----------|
| {리스크 1} | 높음/중간/낮음 | {전략} |
```

### 4. 저장 및 커밋

- `docs/tech-specs/{TICKET}-tech-spec.md`에 저장한다.
- `docs/tech-specs/` 디렉토리가 없으면 생성한다.
- **git commit하지 않는다** — docs/ 산출물은 Phase 4 Archive에서 일괄 커밋한다.

### 5. bf-lead-review 자동 스폰 (Tech-Spec 모드)

<HARD-GATE>
Tech Spec 작성 후 반드시 bf-lead-review를 스폰하여 다관점 리뷰를 수행한다. 리뷰 없이 사람에게 직접 Tech Spec을 제시하지 않는다. "간단한 변경이라 리뷰가 필요 없다"는 이 게이트를 우회하는 전형적인 합리화이다.
</HARD-GATE>

- `bf-lead-review`를 스폰한다:
  - Task tool 사용, `model: opus`
  - 파라미터: `mode: "tech-spec"`, tech-spec 경로 전달
- 메인 세션은 `"done"` + review.md 경로만 수신한다 (컨텍스트 격리).

### 6. 리뷰 결과 제시 및 사람 개입 ①

<HARD-GATE>
리뷰 결과를 사람에게 반드시 제시하고 승인/수정 판단을 받아야 한다. Blocker가 0이어도 자동 승인하지 않는다. 이것이 사람 판단 ①이며, BF 워크플로우에서 사람이 개입하는 정확히 2개 지점 중 하나이다.
</HARD-GATE>

- review.md를 읽어서 사람에게 제시한다.
- 사람의 결정:
  - **승인** → "`Tech Spec이 승인되었습니다. /bf-execute로 구현을 시작하세요.`" 안내
  - **수정 요청** → Tech Spec 수정 후 5단계(bf-lead-review 스폰)를 재실행

## Output Format

- `docs/tech-specs/{TICKET}-tech-spec.md` — Tech Spec 문서
- `docs/reviews/{TICKET}-tech-spec-review.md` — 리뷰 결과 (bf-lead-review가 생성)

마크다운 형식. 섹션: 배경, 현재 상태, 목표 상태, 영향 분석, 인수 조건, 기술 제약, 테스트 전략.

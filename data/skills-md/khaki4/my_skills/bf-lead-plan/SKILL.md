---
name: bf-lead-plan
description: Tech Spec을 분석하여 Epic/Story 구조를 생성하고, Story 5개 이상일 때 병렬로 Story 문서를 작성한다. Distribute 조율 패턴.
---

# Lead Plan (Distribute Pattern)

## Overview

승인된 Tech Spec을 분석하여 Epic → Story 구조를 생성하고, 각 Story에 난이도(S/M/L/XL)를 태깅한다. Story 문서가 5개 이상이면 Creator 에이전트를 병렬로 스폰하여 문서를 작성한다.

## When to Use

- `bf-lead-orchestrate`가 스폰
- 직접 호출하지 않는다.

## Prerequisites

- 승인된 Tech Spec: `docs/tech-specs/{TICKET}-tech-spec.md`
- Tech Spec 리뷰 통과 (사람 개입 ① 완료)

## Error Handling

- Tech Spec 파일 미존재: `"error: tech-spec not found at {경로}"` 신호를 orchestrate에 전달 후 종료
- Story Creator 스폰 실패: Lead가 직접 Story 문서를 작성 (4개 이하일 때와 동일하게 순차 처리)
- conventions.md 미존재: 경고만 표시하고 난이도 태깅은 기본 기준으로 진행 (컨벤션 영향도 반영 불가)

## Instructions

### 1. 초기 로딩

- `docs/tech-specs/{TICKET}-tech-spec.md` 읽기
- `docs/conventions.md` 읽기 (있으면) — 기존 도메인/아키텍처 규칙을 난이도 판정과 Story 분리 기준에 반영

### 2. Epic 도출

- 기능 단위 또는 도메인 단위로 에픽을 분리한다.
- 에픽 간 의존성을 명시한다.
- 에픽은 순차적으로 실행됨을 기준으로 순서를 결정한다.
- **Epic 최소 규모**: Epic당 Story 3개 이상을 권장한다. Story 2개 이하인 Epic이 나오면 인접 Epic과 병합을 검토한다. 단, 도메인 경계가 명확하여 병합이 부자연스러운 경우(예: 인증 vs 결제)는 2개도 허용한다. Epic마다 E2E 검증·통합 리뷰·사람 확인 등 고정 오버헤드가 발생하므로, 불필요하게 작은 Epic은 피한다.
- **Story 0개 에픽 처리**: 인프라 준비, 설정 변경 등 Story로 분해할 수 없는 에픽은 sprint-status.yaml에 Story 없이 에픽만 등록하고, `e2e: passed`로 초기화한다 (기본 템플릿의 `pending`이 아닌 `passed`로 직접 설정).

### 3. Story 구조 결정

각 Epic 내 Story를 결정한다:
- Story는 병렬 실행 가능한 단위로 분리한다.
- 각 Story에 명확한 AC를 포함한다.
- Story 간 의존성이 있으면 Dependencies 섹션에 명시한다.

### 4. 난이도 태깅

<HARD-GATE>
모든 Story에 반드시 난이도(S/M/L/XL)를 태깅해야 한다. 난이도 태그 없이 Story 문서를 완성하지 않는다. 난이도는 agent 구성(모델 선택, 팀 규모)을 결정하는 핵심 입력이다.
</HARD-GATE>

각 Story에 난이도를 태깅한다:

| 난이도 | 기준 |
|--------|------|
| S (Simple) | 단일 파일, 명확한 AC, 의존성 없음 |
| M (Medium) | 2~3 파일, 모듈 간 연결 있음 |
| L (Large) | 다수 파일, 아키텍처 영향 큼 |
| XL (Complex) | 크로스 레이어, 보안/성능 고려, 설계 판단 포함 |

- `docs/conventions.md`에 아키텍처 규칙이 정의되어 있으면, 해당 규칙의 영향을 받는 Story의 난이도를 상향 조정한다 (예: 컨벤션에 엄격한 보안 규칙이 있으면 관련 Story를 M→L로).

### 5. Story 문서 작성 (Distribute Pattern)

**Story 5개 이상:**
- Creator 에이전트를 스폰한다 (`model: sonnet`).
- 각 Creator에게 전달:
  - Story AC, Epic 컨텍스트, Story 문서 템플릿 (아래 Output Format 참조)
- Lead가 모든 Creator의 `"done"` + story 파일을 수집한다.

**Story 4개 이하:**
- Lead가 직접 순차적으로 Story 문서를 작성한다.

### 6. Sprint 식별자 결정

Sprint 식별자는 **Jira 티켓 번호**를 그대로 사용한다 (예: `HACKLE-13554`):
- 스폰 시 전달받은 `{TICKET}` 번호를 sprint-status.yaml의 최상위 키로 사용
- `docs/archive/` 디렉토리에 이미 같은 티켓의 아카이브가 있으면 에러 보고

### 7. sprint-status.yaml 생성

<HARD-GATE>
sprint-status.yaml의 모든 메트릭 필드(model_used, ralph_retries, ralph_approaches, review_blockers, review_recommended, failure_tag, is_regression, parent_story, ralph_stuck)를 기본값(0/null/false)으로 초기화해야 한다. 필드 누락은 이후 bf-metrics 분석을 오염시킨다.
</HARD-GATE>

```yaml
{TICKET}:
  epic-1:
    story-1:
      status: todo
      difficulty: S
      tdd: pending
      review: pending
      model_used: null
      ralph_retries: 0
      ralph_approaches: 0
      review_blockers: 0
      review_recommended: 0
      failure_tag: null
      is_regression: false
      parent_story: null
      ralph_stuck: false
    story-2:
      status: todo
      difficulty: M
      tdd: pending
      review: pending
      model_used: null
      ralph_retries: 0
      ralph_approaches: 0
      review_blockers: 0
      review_recommended: 0
      failure_tag: null
      is_regression: false
      parent_story: null
      ralph_stuck: false
    e2e: pending
```

> 메트릭 필드 기본값: 모든 필드는 0/null/false로 초기화. 각 필드는 이후 Lead 스킬들이 기록한다:
> - `model_used`, `ralph_retries`, `ralph_approaches`, `ralph_stuck`: bf-lead-implement
> - `review_blockers`, `review_recommended`: bf-lead-review
> - `failure_tag`, `is_regression`, `parent_story`: E2E agent

### 8. 파일 저장 및 커밋

- Story 파일: `docs/stories/{TICKET}-story-{N}.md`
- sprint-status.yaml: `docs/sprint-status.yaml`
- **git commit하지 않는다** — docs/ 산출물은 Phase 4 Archive에서 일괄 커밋한다.

### 9. Done 신호

- 스폰한 상위 에이전트에 전달: `"done"` + stories/ 경로 + sprint-status.yaml 경로
- 종료 (컨텍스트 소멸).

## Output Format

### Story 문서 템플릿

```markdown
# {TICKET}-story-{N}: {Story 제목}

## 에픽
{소속 에픽 ID 및 이름}

## 난이도
{S | M | L | XL} — {난이도 판정 근거}

## 인수 조건
- [ ] AC 1: {구체적이고 테스트 가능한 기준}
- [ ] AC 2: ...

## 기술 노트
- 변경 대상 파일/모듈
- 주요 라이브러리 (구현에 핵심적인 외부 라이브러리 — 예: zod, react-hook-form, @tanstack/react-query)
- 의존성 (다른 Story와의 관계)
- 주의사항

## 의존성
- {의존하는 Story ID} (있는 경우)
```

---
name: bf-execute
description: BF 워크플로우의 사람-시스템 경계 허브. orchestrate를 모드별로 스폰하고, 에픽 단위 루프를 돌며 사람과 소통하는 유일한 경계이다.
---

# BF Execute (Entry Point)

## Overview

BF 워크플로우의 실행 진입점이자 **사람-시스템 경계 허브**이다. `bf-lead-orchestrate`를 모드별로 스폰하여 에픽 단위 루프를 돌며, 각 에픽 완료 후 사람에게 결과를 제시한다. 시스템 내부 에이전트는 사람과 직접 소통하지 않으며, bf-execute가 유일한 소통 경계이다.

## When to Use

- 사용자가 `/bf-execute`를 입력했을 때
- `/bf-spec`으로 Tech Spec이 승인된 후 다음 단계로 진행할 때

## Prerequisites

- 승인된 Tech Spec: `docs/tech-specs/{TICKET}-tech-spec.md`
- Tech Spec 리뷰 통과 (사람 개입 ① 완료)

## Error Handling

- Tech Spec 미존재: "Tech Spec 파일이 없습니다. `/bf-spec`으로 먼저 Tech Spec을 작성하고 리뷰를 받으세요." 안내
- Tech Spec 리뷰 미존재 (`docs/reviews/{TICKET}-tech-spec-review.md` 없음): "Tech Spec 리뷰가 수행되지 않았습니다. `/bf-spec`에서 리뷰를 포함한 전체 흐름을 실행하세요." 안내
- orchestrate 스폰 실패: "에이전트 생성에 실패했습니다. 잠시 후 다시 시도하거나, Claude Code를 재시작하세요." 안내

## Instructions

### 1. 사전 확인

- `docs/tech-specs/{TICKET}-tech-spec.md` 존재 확인
- 사용자에게 Jira 티켓 번호를 확인한다 (미제공 시 요청).

### 2. Plan 단계 — orchestrate (plan 모드) 스폰

- Task tool 사용, `model: sonnet` (plan 모드는 단순 라우터 역할이므로 Sonnet으로 충분)
- 전달: `mode: "plan"`, tech-spec 경로, conventions.md 경로 (있으면)
- 수신 대기: `"done"` + sprint-status.yaml 경로 + stories/ 경로
- 수신 후: sprint-status.yaml을 읽어 에픽/스토리 구조를 사람에게 제시한다.

### 3. 에픽 루프

sprint-status.yaml의 에픽을 순서대로 순회한다. 각 에픽에 대해:

#### 3a. orchestrate (epic 모드) 스폰

- Task tool 사용, `model: opus`
- 전달: `mode: "epic"`, `epic_id`, tech-spec 경로, conventions.md 경로
  - 수정 재실행인 경우: `modification_path` 추가 전달
- 수신 대기: `"done"` + sprint-status.yaml 경로 + review.md 경로

#### 3b. 에픽 결과 제시

<HARD-GATE>
에픽 결과를 사람에게 반드시 제시하고 판단을 받아야 한다. 결과가 깨끗해 보여도(Blocker 0, E2E passed) 자동으로 다음 에픽으로 진행하지 않는다. 이것이 사람 판단 ②이며, BF 워크플로우에서 사람이 개입하는 정확히 2개 지점 중 하나이다.
</HARD-GATE>

orchestrate 완료 후 sprint-status.yaml과 review.md를 읽어 사람에게 제시한다:

```
## Epic {EPIC-ID} 완료

### Story 결과
| 스토리 | 상태 | 난이도 | 재시도 횟수 | Stuck |
|--------|------|--------|------------|-------|
| story-1 | done | S | 0 | - |
| story-2 | done | M | 2 | - |
| story-3 | skipped (stuck) | L | 5 | stuck.md 참조 |

### E2E: {passed | skipped | escalated | max-regression-cycles}
### Integration Review: Blockers {N}건, Recommended {N}건
### 상세: docs/reviews/{EPIC-ID}-review.md

> ⚠️ (모든 Story가 skipped인 경우에만 표시)
> 이 에픽의 모든 Story가 skipped(stuck) 상태입니다. 진행 시 해당 기능이 구현되지 않은 상태로 넘어갑니다.

진행하시겠습니까?
1. 다음 에픽으로 진행
2. 수정 후 재실행 (수정 내용 입력)
3. 워크플로우 중단
```

#### 3c. 사람 판단 처리

사람의 선택에 따라:

**1. 다음 에픽으로 진행:**
- 해당 에픽의 사람 수용 상태를 sprint-status.yaml에 반영한다 (`yq -i` 사용):
  - `status: skipped`인 Story의 `review`를 `"approved"`로 설정 (사람이 skip을 수용)
  - `review: pending`인 `status: done` Story의 `review`를 `"approved"`로 설정 (사람이 Blocker를 수용)
  ```bash
  # skipped Story review 정리
  yq -i '.<TICKET>.<EPIC>.<SKIPPED-STORY>.review = "approved"' docs/sprint-status.yaml
  # Blocker 수용 — done Story의 pending review를 approved로 전환
  yq -i '.<TICKET>.<EPIC>.<DONE-STORY>.review = "approved"' docs/sprint-status.yaml
  ```
- 다음 에픽의 3a로 이동한다.

**2. 수정 후 재실행:**
- 사람이 수정 내용을 텍스트로 입력한다.
- bf-execute가 수정 내용을 분석하여 대상 Story를 추론하고, 사람에게 확인한다:
  - "수정 대상 Story: story-1, story-3으로 판단됩니다. 맞습니까?"
  - 사람이 수정하면 그에 따른다.
- `docs/reviews/{EPIC-ID}-modification.md`에 기록한다:

  ```markdown
  # {EPIC-ID} Modification

  ## 수정 지시
  {사람이 입력한 수정 내용 원문}

  ## 대상 Story
  - {확인된 수정 대상 Story ID 목록}
  ```

- **git commit하지 않는다** — docs/ 산출물은 Phase 4 Archive에서 일괄 커밋한다.
- 같은 에픽에 대해 orchestrate를 epic 모드로 다시 스폰한다 (`modification_path` 전달).
- 3b로 돌아가 결과를 다시 제시한다.

**3. 워크플로우 중단:**
- 현재 상태를 안내하고 종료한다.
- `/bf-resume`으로 재개 가능함을 안내한다.

### 4. 전체 완료

모든 에픽 완료 후:

```
워크플로우가 완료되었습니다.

다음 단계:
1. /bf-archive-sprint — 스프린트 아카이빙
2. /bf-metrics — 메트릭 분석 (선택)
3. /bf-update-conventions — 컨벤션 업데이트
```

## Output Format

- 사용자에게 에픽별 결과 제시 + 판단 요청
- 완료 시 다음 단계 안내
- 모든 산출물은 orchestrate 이하 Lead들이 생성 (메인 세션은 modification.md만 직접 생성)

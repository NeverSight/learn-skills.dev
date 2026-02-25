---
name: bf-resume
description: 중단된 BF 워크플로우를 복구한다. sprint-status.yaml에서 마지막 완료 지점을 분석하여 bf-execute와 동일한 에픽 단위 루프로 재개한다.
---

# Resume Workflow

## Overview

세션 중단, context limit 도달, 에러 등으로 BF 워크플로우가 중간에 멈춘 경우, sprint-status.yaml의 상태를 분석하여 적절한 지점부터 워크플로우를 재개한다. bf-execute와 동일한 에픽 단위 루프를 사용하여 사람-시스템 경계를 유지한다.

## When to Use

- Claude Code 세션이 중단된 후 워크플로우를 이어서 진행할 때
- 사용자가 `/bf-resume`을 입력했을 때
- 사용자가 `/bf-resume --from {EPIC-ID}`로 특정 에픽부터 재개하고 싶을 때

## Prerequisites

- `docs/sprint-status.yaml` 존재
- `docs/tech-specs/{TICKET}-tech-spec.md` 존재

## Error Handling

- sprint-status.yaml 미존재: "진행 중인 스프린트가 없습니다. `/bf-spec`으로 새 워크플로우를 시작하세요." 안내
- tech-spec 미존재: "Tech Spec 파일이 없습니다. `/bf-spec`으로 먼저 Tech Spec을 작성하세요." 안내
- `--from`에 존재하지 않는 EPIC-ID 지정: "에픽 '{EPIC-ID}'이(가) sprint-status.yaml에 없습니다. 사용 가능한 에픽: {에픽 목록}" 안내
- yq 미설치: "yq가 설치되지 않았습니다. `brew install yq` (macOS) 또는 https://github.com/mikefarah/yq#install (Linux)로 설치하세요." 안내

## Instructions

### 1. 상태 분석

**yq 전제조건 체크** (최초 1회):
```bash
command -v yq >/dev/null 2>&1 || { echo "❌ yq not installed. Install: brew install yq"; exit 1; }
```

`docs/sprint-status.yaml`을 읽고 현재 스프린트 상태를 분석한다.

### 2. --from 옵션 처리

`--from {EPIC-ID}` 옵션이 주어진 경우 **해당 에픽 전체를 처음부터 재실행**한다:
- 해당 에픽 내 **모든** Story (done 포함)의 `status`를 `todo`로, `tdd`를 `pending`으로, `review`를 `pending`으로 리셋:
  ```bash
  # 에픽 내 각 Story별로 개별 yq 명령 실행 (select+할당 조합의 in-place 동작 불안정 방지)
  yq -i '.<TICKET>.<EPIC>.<STORY-1>.status = "todo" | .<TICKET>.<EPIC>.<STORY-1>.tdd = "pending" | .<TICKET>.<EPIC>.<STORY-1>.review = "pending"' docs/sprint-status.yaml
  # 각 Story에 대해 반복 실행
  ```
- 에픽의 e2e 상태도 `pending`으로 리셋:
  ```bash
  yq -i '.<TICKET>.<EPIC>.e2e = "pending"' docs/sprint-status.yaml
  ```
- `.ralph-progress/` 디렉토리 내 해당 에픽 Story의 진행 파일(`{STORY-ID}.json`)이 있으면 삭제 (이전 Ralph Loop 진행 파일 정리).
- 메트릭 필드는 보존한다 (이전 시도의 기록).
- 재개 지점을 **해당 에픽**으로 설정한다.

> **참고**: `--from`은 에픽 전체 재실행이다. 미완료 Story만 재실행하려면 `--from` 없이 실행하면 자동 판별된다.

### 3. 자동 재개 지점 판별

옵션 없이 실행된 경우, 다음 우선순위로 재개 지점을 자동 판별한다 (**위에서부터 순서대로 검사하여 첫 번째 매칭 적용**):

**a) Story가 하나도 없는 경우 (sprint-status.yaml은 있지만 Story 미생성):**
- 재개 지점: **Plan 단계** — orchestrate plan 모드부터 시작

**b) `status: in_progress`인 Story가 있는 경우:**
- git status로 uncommitted 변경사항 확인
- 변경사항 있음: 사용자에게 "이전 진행 중이던 {STORY-ID}의 미커밋 변경사항이 있습니다." 확인 후 처리:
  - **"변경사항 유지"** (기본): Story별 브랜치에 보관한다:
    ```bash
    git checkout -b bf-stash/{STORY-ID}
    git add --all -- ':!docs/' && git commit -m "[{TICKET}] 중단된 작업 백업"
    git checkout {원래-브랜치}
    ```
    사용자에게 "`bf-stash/{STORY-ID}` 브랜치에 백업했습니다. 필요 시 `git cherry-pick`으로 복원 가능합니다." 안내
  - **"변경사항 폐기"**: `git checkout -- .`으로 미커밋 변경 제거
  - 어느 경우든 `status: todo`, `tdd: pending`, `review: pending`으로 리셋 → 에픽 재개 시 새 agent가 처음부터 구현
  - 복수 Story가 동시에 in_progress인 경우: 각 Story별로 변경 파일을 식별하여 개별 브랜치에 보관. 파일 귀속이 불분명하면 `bf-stash/mixed-{EPIC-ID}`에 전체 보관
- `ralph_stuck: true`인 경우: bf-lead-implement 크래시로 orchestrate에 보고되지 못한 상태. `status: skipped`로 설정하여 orchestrate가 재처리하지 않도록 한다.
- 변경사항 없음 (`ralph_stuck: false`): git log에서 해당 Story ID 커밋 존재 여부 확인
  ```bash
  git log --oneline --grep="{STORY-ID}" | head -1
  ```
  - **커밋 존재**: agent가 커밋 후 보고 전에 중단된 것 (Lead 크래시 포함). `status: done`, `tdd: done`으로 설정. `.ralph-progress/{STORY-ID}.json`이 있으면 `ralph_retries`와 `ralph_approaches`를 sprint-status.yaml에 반영 (`model_used`는 bf-lead-implement가 결정하므로 이 경우 `null`로 유지)
  - **커밋 미존재**: 구현이 시작되지 않았거나 중간에 중단된 것. `status: todo`, `tdd: pending`, `review: pending`으로 리셋
- `.ralph-progress/` 디렉토리에 해당 Story 진행 파일이 있으면 삭제 (리셋 Story만)
- 재개 지점: **해당 에픽**

**c) 미완료 에픽이 있는 경우 (일부 Story가 `todo`이거나 e2e/review가 미완):**
- 재개 지점: **해당 에픽** (orchestrate epic 모드가 sprint-status.yaml을 읽고 이미 done인 Story를 건너뜀)

**d) 모든 에픽의 e2e가 terminal state (`passed` | `skipped` | `escalated` | `max-regression-cycles`)이고 모든 Story `review: approved`인 경우:**
- "모든 에픽이 완료되었습니다. `/bf-archive-sprint`를 실행하세요." 안내
- 종료.

### 4. 재개 지점 제시

```
워크플로우 재개 지점 분석
- 티켓: {TICKET}
- 현재 상태: {상태 요약}
- 재개 에픽: {epic-id} (총 N개 중 M번째)
- skipped Story: {있으면 목록 표시}
- 이유: {판별 근거}

계속 진행하시겠습니까?
```

skipped(stuck) Story가 있으면 함께 표시한다. 이전 실행에서 이미 auto-skip 되었으므로, 사람이 수정을 원하면 에픽 결과 확인 시점에서 modification.md로 지시할 수 있다.

### 5. 재개 실행

사용자 확인 후, 재개 지점에 따라:

**Plan 미완:**
- orchestrate (plan 모드) 스폰 (`model: sonnet` — plan 모드는 단순 라우터 역할)
- 전달: tech-spec 경로, conventions.md 경로
- 수신 후: sprint-status.yaml의 에픽/스토리 구조를 사람에게 제시
- 이후 에픽 루프 진입 (Step 6)

**에픽 재개:**
- bf-execute와 동일한 에픽 루프 진입 (Step 6)

### 6. 에픽 루프 (bf-execute와 동일)

재개 에픽부터 순서대로 순회한다. 각 에픽에 대해:

#### 6a. orchestrate (epic 모드) 스폰

- Task tool 사용, `model: opus`
- 전달: `mode: "epic"`, `epic_id`, tech-spec 경로, conventions.md 경로
  - 수정 재실행인 경우: `modification_path` 추가 전달
- 수신 대기: `"done"` + sprint-status.yaml 경로 + review.md 경로

#### 6b. 에픽 결과 제시

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

#### 6c. 사람 판단 처리

사람의 선택에 따라:

**1. 다음 에픽으로 진행:**
- 해당 에픽의 사람 수용 상태를 sprint-status.yaml에 반영한다 (`yq -i` 사용):
  - `status: skipped`인 Story의 `review`를 `"approved"`로 설정 (사람이 skip을 수용)
  - `review: pending`인 `status: done` Story의 `review`를 `"approved"`로 설정 (사람이 Blocker를 수용)
  ```bash
  yq -i '.<TICKET>.<EPIC>.<SKIPPED-STORY>.review = "approved"' docs/sprint-status.yaml
  yq -i '.<TICKET>.<EPIC>.<DONE-STORY>.review = "approved"' docs/sprint-status.yaml
  ```
- 다음 에픽의 6a로 이동한다.

**2. 수정 후 재실행:**
- 사람이 수정 내용을 텍스트로 입력한다.
- bf-resume이 수정 내용을 분석하여 대상 Story를 추론하고, 사람에게 확인한다.
- `docs/reviews/{EPIC-ID}-modification.md`에 기록한다 (bf-execute의 modification.md 형식과 동일).
- **git commit하지 않는다** — docs/ 산출물은 Phase 4 Archive에서 일괄 커밋한다.
- 같은 에픽에 대해 orchestrate를 epic 모드로 다시 스폰한다 (`modification_path` 전달).
- 6b로 돌아가 결과를 다시 제시한다.

**3. 워크플로우 중단:**
- 현재 상태를 안내하고 종료한다.

### 7. 전체 완료

모든 에픽 완료 후, bf-execute와 동일하게 후처리 단계를 안내한다.

```
워크플로우가 완료되었습니다.

다음 단계:
1. /bf-archive-sprint — 스프린트 아카이빙
2. /bf-metrics — 메트릭 분석 (선택)
3. /bf-update-conventions — 컨벤션 업데이트
```

## Output Format

대화로 재개 지점 분석 결과를 출력하고, 사용자 확인 후 에픽 단위 루프를 실행한다. modification.md 외 별도 파일 생성 없음.

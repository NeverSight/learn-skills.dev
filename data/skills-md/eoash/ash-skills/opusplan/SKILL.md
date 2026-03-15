---
name: opusplan
description: Opus가 계획, Sonnet이 구현. 복잡한 작업을 Opus에게 설계시킨 뒤 현재 세션에서 단계별 실행. "opusplan", "opus 계획", "opus plan" 요청에 사용.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - AskUserQuestion
  - Task
---

# opusplan

**Opus가 계획, Sonnet이 구현** — 복잡한 작업을 위한 2단계 워크플로우.

## Workflow

1. **Phase 1 — Planning (Opus)**: Claude Opus가 구조화된 단계별 구현 계획 생성
2. **Phase 2 — Review**: 계획을 사용자에게 보여주고 확인
3. **Phase 3 — Implementation (Sonnet)**: 현재 세션에서 계획대로 단계별 실행

## Why

- Opus는 깊은 사고와 종합적인 설계에 강함
- Sonnet은 명확한 지시를 빠르게 실행하는 데 강함
- 한 번 깊게 생각하고, 효율적으로 실행

## Usage

```
/opusplan "JWT 인증을 Express API에 추가해줘"
/opusplan "AR 매칭 로직 정확도 개선" --plan-only
/opusplan "Slack 알림 에러 처리 강화" --no-confirm
/opusplan "DB 스키마 리팩토링" --context ./docs/schema.md
```

## Arguments

Parse from $ARGUMENTS:
- **Task** (required) — 계획하고 구현할 작업
- `--no-confirm` — 확인 없이 바로 구현
- `--plan-only` — 계획만 생성, 구현 안 함
- `--context PATH` — 추가 컨텍스트 파일/디렉토리

## Phase 1: Generate Plan with Opus

Run the planning script. Use `--output` to write to a temp file (Windows 인코딩 이슈 방지):

```bash
python "${SKILL_DIR}/scripts/run_opusplan.py" --task "TASK_HERE" --output "/tmp/opusplan_result.json" [--context PATH]
```

Then read the result file using the Read tool: `/tmp/opusplan_result.json`

While waiting, show a status message: "Opus가 계획을 수립 중입니다..."

**IMPORTANT**: Use `python` (not `python3`) on Windows.

## Phase 2: Present and Confirm Plan

Parse the JSON from the result file and display:

---

**Opus Implementation Plan**

**Task:** [task description]

**Overview:** [brief summary]

**Steps:**
1. [Step 1 title]
   - Details...
2. [Step 2 title]
   - Details...

**Complexity:** [simple/moderate/complex]
**Files:** [list if known]
**Risks:** [potential issues]

---

Then ask for confirmation (unless `--no-confirm`):

Use AskUserQuestion:
- question: "이 계획대로 구현을 시작할까요?"
- header: "실행 확인"
- options:
  - label: "네, 시작하세요 (Recommended)", description: "계획대로 바로 구현합니다"
  - label: "계획만 저장", description: "구현 없이 계획 파일만 저장합니다"
  - label: "계획 수정 후 실행", description: "계획을 수정한 다음 실행합니다"

If `--plan-only`, save plan to file and stop.

## Phase 3: Implement the Plan

Execute each step sequentially:

1. Announce: "**Step N/Total: [step title]**"
2. Execute using appropriate tools (Read, Edit, Write, Bash, etc.)
3. Verify step succeeded
4. Next step

**Guidelines:**
- Follow the plan faithfully, adapt if unexpected issues arise
- If a step fails, explain and fix or skip with explanation
- After all steps, provide summary

## Output Format

### Success:

**opusplan Complete**

**Plan by:** Claude Opus | **Implemented by:** Claude Sonnet

**Steps completed:** N/N

**Summary:** [what was accomplished]

**Files modified:**
- path/to/file1
- path/to/file2

### Partial:

**opusplan — Partial Completion**

**Completed:** ✓ Step 1, ✓ Step 2
**Not completed:** ✗ Step 3 (reason)

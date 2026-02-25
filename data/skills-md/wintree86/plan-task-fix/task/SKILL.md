---
name: task
description: >
  Task tracker -- track progress and verify implementation directly on plan.md.
  범용 프로젝트 태스크 관리. plan 문서에서 진행률 추적, 현황 요약.
  Triggers: /task, "task", "태스크", "progress", "진행률", "진행 상황"
---

# Task Manager

Track tasks, manage progress, and verify implementation directly on plan.md.
plan.md를 기반으로 태스크 진행률을 추적합니다.

## Usage / 사용법

```
/task              # Summary / 현황 요약 (default)
/task summary      # Summary / 현황 요약
/task update       # Update progress / 진행률 업데이트
/task done         # Mark done / 완료 처리
/task verify       # Verify implementation / 구현 검증
/task wrap         # Wrap-up session / 세션 랩업 파이프라인 작동
```

The first argument determines the command: `$ARGUMENTS`

---

## Project Detection / 프로젝트 감지 규칙

1. **CWD-based** - Uses current working directory as project root / 현재 작업 디렉토리를 프로젝트 루트로 사용
2. **Git root detection** - `git rev-parse --show-toplevel` / Git root로 프로젝트 루트 확인
3. **Project name** - Git root folder name / git root 폴더명 사용

### Document folder search order / 문서 폴더 탐색 순서:
1. `.claude-docs/`
2. `.claude/docs/`
3. `docs/`
4. CWD (project root / 프로젝트 루트)

### plan.md search order / plan.md 탐색 순서:
1. `.claude-docs/plan.md`
2. `.claude/docs/plan.md`
3. `docs/plan.md`
4. `PLAN.md`
5. `plan.md`

---

## Command: update

Updates plan.md progress.
plan.md의 진행률을 업데이트합니다.

### Steps / 수행 단계:
1. Read plan.md / plan.md 파일 읽기
2. Count checked items `[x]` / 체크된 항목 카운트
3. Update Progress Overview table / Progress Overview 테이블 업데이트
4. Update Phase Status / Phase Status 업데이트:
   - All incomplete: `pending` / 모든 태스크 미완료
   - Some complete: `in-progress` / 일부 완료
   - All complete: `completed` / 모두 완료
5. Update `Last Updated` date / 날짜 갱신
6. Append change log to progress.md / progress.md에 변경 이력 추가

### progress.md format / progress.md 형식:
```markdown
# Progress Log

## YYYY-MM-DD
- Phase N: X/Y completed / 완료 (Z%)
- Completed / 완료된 태스크: Task1, Task2
- Next / 다음 태스크: Task3

## YYYY-MM-DD (previous / 이전)
...
```

---

## Command: summary (default / 기본)

Summarizes current progress.
현재 진행 현황을 요약합니다.

**Runs when no arguments or `summary`. / 인수가 없거나 `summary`인 경우 실행됩니다.**

### Output format / 출력 형식:
```
📊 {Project Name} Progress / 개발 현황

Overall / 전체 진행률: 12/29 (41%)

Phase 1: MVP ✅ Completed / 완료 (5/5)
Phase 2: Core Features 🔄 In Progress / 진행중 (3/5)
Phase 3: Advanced ⏳ Pending / 대기 (0/4)

🔄 In Progress / 현재 진행 중:
- Remaining tasks in active Phase

📋 Next Tasks / 다음 태스크:
1. Next task 1
2. Next task 2
3. Next task 3
```

### Status icons / 상태 아이콘:
- ✅ Completed / 완료 (completed)
- 🔄 In Progress / 진행중 (in-progress)
- ⏳ Pending / 대기 (pending)

---

## File Location Rules / 파일 위치 규칙

| File | Default Location | Description |
|------|-----------------|-------------|
| plan.md | document folder | Source plan / 원본 문서 |
| progress.md | document folder | Progress log / 진행 이력 |

Creates `.claude-docs/` automatically if no document folder exists.
문서 폴더가 없으면 `.claude-docs/`를 자동 생성합니다.

---

## Notes / 주의사항

1. **Direct editing** - Change `[ ]` to `[x]` manually / plan.md 직접 편집 가능
2. **Update after changes** - Run `/task update` to refresh tables / 진행률 변경 후 테이블 갱신
3. **plan.md format** - Requires checklist (`- [ ]`) patterns / 체크리스트 패턴 필요

---

## Command: done

Auto-detects completed tasks from current session and updates plan.md.
현재 세션에서 완료된 태스크를 자동 감지하여 plan.md를 업데이트합니다.

**Follows task-tracker rules below. / 아래 task-tracker 규칙을 따릅니다.**

### Steps / 수행 단계:

1. **Find plan.md / plan.md 파일 찾기**
   - Search in order: `.claude-docs/plan.md` → `.claude/docs/plan.md` → `docs/plan.md` → `PLAN.md` → `plan.md`
   - If not found, output error message / 파일이 없으면 에러 메시지 출력

2. **Analyze current conversation / 현재 대화에서 구현된 기능 파악**
   - Check Edit/Write tool usage history / Edit/Write 도구 사용 이력 확인
   - Analyze code changes / 코드 변경 내용 분석
   - Check for completion mentions ("done", "completed", "구현 완료") / 완료 언급 확인

3. **Match to tasks / 해당하는 태스크 찾기**
   - Match against `- [ ]` incomplete tasks / 미완료 태스크 중 매칭
   - Compare task names with implemented features / 태스크명과 구현 내용 비교
   - **Exact matching only** - Mark complete only when task name clearly matches implementation / 태스크명과 구현 내용이 명확히 일치할 때만 완료 처리
   - **Conservative judgment** - Do not mark if uncertain / 불확실한 경우 완료 처리하지 않음

4. **Mark tasks complete / 태스크 완료 처리**
   - Change `[ ]` → `[x]` for matched tasks / 매칭된 태스크만 변경
   - Edit only the exact matching lines / 해당 라인만 정확히 수정
   - Multiple tasks can be marked at once / 한 번에 여러 태스크 완료 가능

5. **Update Progress Overview table / Progress Overview 테이블 업데이트**
   - Recalculate completed/total count per Phase / Phase별 완료/전체 카운트 재계산
   - Update percentages / 퍼센트 업데이트
   - Update Phase Status:
     - All incomplete: `pending` / 모든 태스크 미완료
     - Some complete: `in-progress` / 일부 완료
     - All complete: `completed` / 모두 완료

6. **Update Last Updated date / 날짜 갱신**

### Output format / 출력 형식:
```
✅ Done / 완료: [Task name]
📊 Progress / 진행률: Phase N - X/Y (Z%)

plan.md updated / 업데이트 완료
```

Multiple tasks / 여러 태스크 완료 시:
```
✅ Done / 완료:
- [Task name 1]
- [Task name 2]

📊 Progress / 진행률:
- Phase N: X/Y (Z%)
- Overall / 전체: A/B (C%)

plan.md updated / 업데이트 완료
```

### Example / 사용 예시:
```
Developer: "Implement card selection screen"
Claude: [code written]

Developer: "/task done"
Claude:
  ✅ Done / 완료: 2.2 Three Card Selection
  📊 Phase 2: 1/6 (17%)
  plan.md updated / 업데이트 완료
```

### Important notes / 주의사항:
- **No undo** - `[x]` → `[ ]` changes must be done manually / 되돌리기는 수동으로만 가능
- **Conservative** - When in doubt, do NOT mark as complete / 불확실하면 완료 처리하지 않음

---

## Command: verify

Compares plan.md requirements against actual code implementation.
plan.md와 실제 코드를 비교하여 구현 상태를 검증합니다.

**Follows task-tracker rules below. / 아래 task-tracker 규칙을 따릅니다.**

### Steps / 수행 단계:

1. **Read plan.md / plan.md 읽기**
   - Search in order: `.claude-docs/plan.md` → `.claude/docs/plan.md` → `docs/plan.md` → `PLAN.md` → `plan.md`

2. **Extract tasks from current Phase / 현재 Phase의 태스크 목록 추출**
   - Find Phase with `in-progress` status / `in-progress` 상태인 Phase 찾기
   - Extract `- [ ]` and `- [x]` items / 해당 Phase의 체크리스트 항목 추출

3. **Inspect actual code files / 실제 코드 파일 확인**
   - **Glob**: Check if related files exist / 관련 파일 존재 여부
   - **Grep**: Verify core functions/classes are implemented / 핵심 함수/클래스 구현 여부
   - **Read**: Check detailed implementation / 상세 구현 확인

4. **Determine implementation status / 구현 상태 판단**
   - ✅ Completed / 완료: File exists + core logic implemented / 파일 존재 + 핵심 로직 구현됨
   - 🔄 In Progress / 진행중: File exists but partial / 파일 존재하지만 일부만 구현
   - ❌ Not Started / 미시작: No file or empty / 파일 없음 또는 빈 구현

### Output format / 출력 형식:
```
📋 Phase N: [Phase Name] Implementation Status / 구현 현황

✅ Completed / 완료:
- Task 1 (lib/path/file.dart)

🔄 In Progress / 진행중:
- Task 2 (lib/path/file2.dart - partial / 일부 구현)

❌ Not Started / 미시작:
- Task 3

📊 Verification / 검증 결과: 1/3 completed / 완료 (33%)
```

---

## Command Reference / 명령어 비교

| Command | Action | Purpose |
|---------|--------|---------|
| `/task` | Summary / 현황 요약 | Quick status check / 빠른 상태 확인 |
| `/task summary` | Summary / 현황 요약 | Quick status check / 빠른 상태 확인 |
| `/task update` | Recalculate progress / 진행률 재계산 | After manual checks / 수동 체크 후 |
| `/task done` | Mark complete / 완료 처리 | After development / 개발 완료 후 |
| `/task verify` | Verify implementation / 구현 검증 | Code vs plan / 코드 vs 계획 비교 |
| `/task wrap` | Session Wrap-up / 세션 랩업 | After coding session / 코딩 세션 종료 후 |

---

## Command: wrap

Executes a 2-phase pipeline to wrap up the current coding session, optimizing context and generating follow-up priorities.
현재 코딩 세션을 마무리하고 컨텍스트 메모리를 최적화하며 다음 목표를 제안하는 2단계 파이프라인을 실행합니다.

### 2-Phase Pipeline Architecture / 2단계 파이프라인 구조

#### Phase 1: Parallel Analysis / 병렬 분석
Run the following 4 subagents in parallel using the `RunCommand` tool (e.g., `claude -p skills/task/agents/xxx.md` or invoke them via internal subagent mechanics).
아래 4개의 서브 에이전트를 병렬로 실행하여 결과를 취합합니다.

1. **`progress-analyzer`**: Validates code against plan.md / 실제 코드 구현 검증.
2. **`context-archiver`**: Prepares completed Phase for archiving / 완료된 Phase 압축 준비.
3. **`knowledge-extractor`**: Extracts TILs and gotchas / 배운 점 및 에러 해결책 추출.
4. **`next-planner`**: Suggests top 3 next tasks / 다음 세션 최우선 태스크 3개 제안.

#### Phase 2: Sequential Validation & Approval / 순차적 검증 및 승인
1. **`wrap-coordinator`**: Aggregates Phase 1 results, presents a unified report to the user, and asks for execution confirmation. / Phase 1 결과를 취합하여 리포팅하고 사용자의 승인을 받습니다.
2. IF User approves / 승인 시:
   - Updates `plan.md` (clears completed details)
   - Appends to `archive.md`
   - Appends to `knowledge.md`

---

## Related Skills

Part of the **plan-task-fix** suite:
- `/plan` - Plan document management (plan.md) / 기획서 관리
- `/task` - Task tracking and progress (plan.md) / 태스크 추적
- `/fix` - Bug/improvement backlog (backlog.md) / 백로그 관리

Install: `npx skills add wintree86/plan-task-fix`

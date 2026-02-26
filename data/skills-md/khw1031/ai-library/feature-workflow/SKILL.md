---
name: feature-workflow
description: >
  기능 구현을 5단계(Requirements → Design → Task → Implementation → Review)
  워크플로우로 체계적으로 진행합니다. Agent Team 기반 병렬 구현을 지원합니다.
  워크플로우, 기능 구현, 기능 개발, 작업 재개, TASK-ID 패턴, .ai/tasks 요청 시 활성화.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Feature Workflow

기능 구현을 체계적으로 진행하는 5단계 워크플로우입니다.

## 핵심 원칙

1. **Context Isolation**: 각 Step은 새 대화에서 실행 권장
2. **Human in the Loop**: 사용자 확인 후 진행
3. **Document as Interface**: Step 간 통신은 문서로 수행
4. **Git as History**: 각 Step 완료 시 커밋으로 체크포인트 생성

## 워크플로우 개요

| Step | 역할 | 입력 | 출력 | 상세 |
|------|------|------|------|------|
| 1 | Requirements Analyst | 00-user-prompt.md | 10-output-plan.md | [step-1.md](references/step-1.md) |
| 2 | System Designer | 10-output-plan.md | 20-output-system-design.md | [step-2.md](references/step-2.md) |
| 3 | Task Analyzer | 10+20 | 30-output-task.md + todos/ | [step-3.md](references/step-3.md) |
| 4 | Coordinator (Team Lead) | todos/*.md | 40-output-implementation.md | [step-4.md](references/step-4.md) |
| 5 | Reviewer | 40-output-impl.md | 50-output-review.md | [step-5.md](references/step-5.md) |

## 규칙 로드

각 Step 시작 시 [assets/rules/AGENTS.md](assets/rules/AGENTS.md)를 읽고 규칙을 로드하세요:
- **필수**: `MUST/workflow-rule.md` (항상)
- **도메인**: 작업 컨텍스트에 따라 동적 로드 (react/, testing/, api/ 등)

---

## 새 작업 시작

1. **Task ID 결정**: 사용자에게 요청 (예: `PROJ-001`)
2. **Task 초기화**: `./scripts/task.sh init <TASK_ID>`
3. **입력 작성**: `.ai/tasks/<TASK_ID>/00-user-prompt.md` 편집
4. **규칙 로드**: [assets/rules/AGENTS.md](assets/rules/AGENTS.md) 읽기
5. **Step 1 실행**: [references/step-1.md](references/step-1.md) 참조

## 작업 재개

사용자가 TASK_ID를 언급하거나 "작업 이어서" 요청 시:

1. `status.yaml` 읽기 → 현재 Step/상태 파악
2. 규칙 로드 → 해당 Step 참조 문서로 진행

상세 절차: [references/resume-guide.md](references/resume-guide.md)

## 진행 상태 확인

```bash
./scripts/task.sh status <TASK_ID>
./scripts/task.sh list
```

---

## Step 요약

### Step 1: Requirements Analysis

- **역할**: Requirements Analyst — 사용자 요구사항을 분석하고 구조화
- **입력**: `00-user-prompt.md` → **출력**: `10-output-plan.md`
- **상세**: [references/step-1.md](references/step-1.md)

### Step 2: Design & Planning

- **역할**: System Designer — 요구사항 기반 설계 및 구현 계획 수립
- **입력**: `10-output-plan.md` → **출력**: `20-output-system-design.md`
- **상세**: [references/step-2.md](references/step-2.md)

### Step 3: Task Analysis

- **역할**: Task Analyzer — 설계를 작업 단위로 분해, 병렬화 계획
- **입력**: `10 + 20` → **출력**: `30-output-task.md` + `todos/*.md`
- **상세**: [references/step-3.md](references/step-3.md)

### Step 4: Implementation (Agent Team)

- **역할**: Coordinator — Agent Team을 스폰하여 병렬 구현
- **입력**: `todos/*.md` → **출력**: `40-output-implementation.md` + 코드
- **방식**: `TeamCreate` → `TaskCreate` → `Task`(Worker 스폰) → `SendMessage`(모니터링) → `TeamDelete`(정리)
- **상세**: [references/step-4.md](references/step-4.md) / [Team 스폰 상세 가이드](references/team-spawn.md)

### Step 5: Review (code-review-team)

- **역할**: Reviewer — code-review-team 스킬 기반 전문가 리뷰
- **입력**: `40-output-implementation.md` → **출력**: `50-output-review.md`
- **방식**: Phase 1 전문가 리뷰 → 사용자 확인 → Phase 2 팀 개선 → PR
- **상세**: [references/step-5.md](references/step-5.md)

---

## 상세 가이드

| 문서 | 설명 |
|------|------|
| [references/step-1.md](references/step-1.md) | 요구사항 분석 절차 |
| [references/step-2.md](references/step-2.md) | 설계 및 계획 절차 |
| [references/step-3.md](references/step-3.md) | 태스크 분해 절차 |
| [references/step-4.md](references/step-4.md) | Agent Team 구현 절차 |
| [references/step-5.md](references/step-5.md) | 코드 리뷰 및 PR 절차 |
| [references/team-spawn.md](references/team-spawn.md) | Step 4 Team 스폰 패턴 |
| [references/resume-guide.md](references/resume-guide.md) | 작업 재개 상세 절차 |
| [assets/templates/](assets/templates/) | 출력 문서 템플릿 |
| [scripts/task.sh](scripts/task.sh) | 작업 관리 스크립트 |

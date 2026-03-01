---
name: bmad-orchestrator
keyword: bmad
description: Orchestrates BMAD workflows for structured AI-driven development. Routes work across Analysis, Planning, Solutioning, and Implementation phases.
allowed-tools: [Read, Write, Bash, Grep, Glob]
tags: [bmad, orchestrator, workflow, planning, implementation]
platforms: [Claude, Gemini, Codex, OpenCode]
version: 1.0.0
source: user-installed skill
---

# bmad-orchestrator - BMAD Workflow Orchestration

## When to use this skill

- Initializing BMAD in a new project
- Checking and resuming BMAD workflow status
- Routing work across Analysis, Planning, Solutioning, and Implementation
- Managing structured handoff between phases

---

## Installation

```bash
npx skills add https://github.com/supercent-io/skills-template --skill bmad-orchestrator
```

## Codex 사용 참고

`bmad-orchestrator`의 기본 실행 경로는 Claude Code입니다.  
Codex에서 직접 동일한 흐름으로 사용하려면 `omx`/`ohmg` 등 상위 오케스트레이션 경로를 통해 BMAD 단계를 운영하는 것을 권장합니다.

---

## BMAD Execution Commands

## 플랫폼별 적용 상태 (현재 지원 기준)

| 플랫폼 | 현재 지원 방식 | 적용 조건 |
|---|---|---|
| Gemini CLI | 네이티브(권장) | `bmad` 키워드 등록 후 `/workflow-init` 실행 |
| Claude Code | 네이티브(권장) | 스킬 설치 + `기억해` 패턴 |
| OpenCode | 오케스트레이션 연동 | `omx`/`ohmg`/`omx` 류 브릿지 사용 |
| Codex | 오케스트레이션 연동 | `omx`/`ohmg`류 브릿지 사용 |

`현재 스킬만`으로 가능한지:  
- Gemini CLI/Claude Code: **가능**  
- OpenCode/Codex: **가능(오케스트레이션 경유)**

Use these in your AI session:

```text
/workflow-init
/workflow-status
```

Typical flow:

1. Run `/workflow-init` to bootstrap BMAD config.
2. Move through phases in order: Analysis -> Planning -> Solutioning -> Implementation.
3. Run `/workflow-status` any time to inspect current phase and progress.

---

## Quick Reference

| Action | Command |
|--------|---------|
| Initialize BMAD | `/workflow-init` |
| Check BMAD status | `/workflow-status` |


---

## plannotator Integration (Phase Review Gate)

Each BMAD phase produces a key document (PRD, Tech Spec, Architecture). Before transitioning to the next phase, review that document with **plannotator** and auto-save it to Obsidian.

### Why use plannotator with BMAD?

- **Quality gate**: Approve or request changes before locking in a phase deliverable
- **Obsidian archive**: Every approved phase document auto-saves with YAML frontmatter and `[[BMAD Plans]]` backlink
- **Team visibility**: Share a plannotator link so stakeholders can annotate the PRD/Architecture before implementation begins

### Phase Review Pattern

After completing any phase document, submit it for review:

```bash
# After /prd → docs/prd-myapp-2026-02-22.md is created
bash scripts/phase-gate-review.sh docs/prd-myapp-2026-02-22.md "PRD Review: myapp"

# After /architecture → docs/architecture-myapp-2026-02-22.md is created
bash scripts/phase-gate-review.sh docs/architecture-myapp-2026-02-22.md "Architecture Review: myapp"
```

Or submit the plan directly from within your AI session:

```text
# In Claude Code after /prd completes:
planno — review the PRD before we proceed to Phase 3
```

The agent will call `submit_plan` with the document content, opening the plannotator UI for review.

### Phase Gate Flow

```
/prd completes → docs/prd-myapp.md created
       ↓
 bash scripts/phase-gate-review.sh docs/prd-myapp.md
       ↓
 plannotator UI opens in browser
       ↓
  [Approve]              [Request Changes]
       ↓                        ↓
 Obsidian saved          Agent revises doc
 bmm-workflow-status     Re-submit for review
 updated automatically
       ↓
 /architecture (Phase 3)
```

### Obsidian Save Format

Approved phase documents are saved to your Obsidian vault with:

```yaml
---
created: 2026-02-22T22:45:30.000Z
source: plannotator
tags: [bmad, phase-2, prd, myapp]
---

[[BMAD Plans]]

# PRD: myapp
...
```

### Quick Reference

| Phase | Document | Gate Command |
|-------|----------|--------------|
| Phase 1 → 2 | Product Brief | `bash scripts/phase-gate-review.sh docs/product-brief-*.md` |
| Phase 2 → 3 | PRD / Tech Spec | `bash scripts/phase-gate-review.sh docs/prd-*.md` |
| Phase 3 → 4 | Architecture | `bash scripts/phase-gate-review.sh docs/architecture-*.md` |
| Phase 4 done | Sprint Plan | `bash scripts/phase-gate-review.sh docs/sprint-status.yaml` |
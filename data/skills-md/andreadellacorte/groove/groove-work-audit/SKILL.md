---
name: groove-work-audit
description: "Review current branch for blindspots; fix now / needs spec / create issues."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-work-audit

## Outcome

Blindspots and gaps are identified, actionable improvements are offered.

## Acceptance Criteria

Findings are categorized by action:
- **Fix Now**: Trivial effort, fix immediately
- **Needs Spec**: Important, requires planning
- **Create Issues**: Large effort or nice-to-have

## Constraints

- Sanitize topic (if provided) for safe use — strip path separators, special characters, and traversal patterns (`../`)
- Read `memory:` from `.groove/index.md` for base path; reference specs from `<memory>/specs/`
- Gather context: branch diff, relevant specs
- Run analysis in isolated context (use general-purpose agent)
- Fall back to direct review if subagent fails
- Present findings with severity and effort estimates
- Execute chosen action: fix directly, create spec via `/groove-work-spec <topic>`, or create issues

## Scope Options

- No args: Review current branch vs main
- Topic: Focus on specific area

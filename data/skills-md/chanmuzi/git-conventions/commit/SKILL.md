---
name: commit
description: Create a git commit following project conventions
version: "1.1.0"
---

## Gather Context

Run the following commands to understand the current state:
1. `git status` — check current status and untracked files
2. `git diff HEAD` — review all changes

## Commit Message Convention

Format: `{type}: {description}` or `{type}({scope}): {description}`

### Type Prefixes (always lowercase)

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `style` | Formatting, linting (no logic change) |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `perf` | Performance improvement |
| `chore` | Build, CI, dependencies, config |
| `hotfix` | Urgent production fix |

### Scope (optional)

Add scope in parentheses when the change targets a specific module or component:
- `feat(source-map): ...`
- `fix(full-text): ...`
- `test(query-rewriting): ...`

### Description Rules

- Write the description in the language configured in the project's CLAUDE.md. If no language is configured, follow the user's conversational language.
- Keep the subject line concise — aim for under 50 characters.
- Use natural, fluent phrasing. Do not force-translate well-known technical terms. For example, write `source_map` as-is rather than translating it.
- Focus on WHAT changed and WHY, not HOW.

### Multi-line Body (for complex changes)

When the diff involves multiple files or logical units, add a body after a blank line to explain details:

```
{type}: {subject line}

- {detail 1}
- {detail 2}
- {detail 3}
```

**When to use multi-line:**
- 3+ files changed across different concerns
- Non-obvious reasoning behind the change
- Breaking changes or migration notes

**When single-line is enough:**
- Simple, self-explanatory changes (typo fix, single-file edit, etc.)

### Examples

**Single-line:**
```
feat: 멀티턴 컨텍스트 유지 기능 추가
fix: 요청 DTO 모델 기본값을 settings 기반으로 통일
refactor: 미사용 openai_api_key/openai_base_url 프로퍼티 제거
style: black 포맷팅 적용
perf: Classification max_tokens 30 → 15로 조정
chore: 보안 취약점 패키지 업데이트 (urllib3, langchain-core)
docs: README 환경변수 가이드 업데이트
test: 멀티턴 컨텍스트 유지 기능 테스트 추가
feat(source-map): 검색하지 않은 턴에서도 source_map 지속 반환
fix(full-text): 전문 조회 실패 시 state 누출 방지
hotfix: uv lock synced
```

**Multi-line:**
```
refactor: Gather Context 불필요한 명령 및 중복 step 제거

- commit: git branch, git log 명령 삭제 (gitStatus/컨벤션 정의로 대체)
- pr: git remote show origin, gh pr list 네트워크 호출 제거
- review: Gather Context 섹션 삭제, 카테고리 불일치 수정
```

## Task

1. Analyze the diff and draft a commit message following the convention above.
2. Present the proposed commit message to the user.
3. Stage the relevant files individually and create the commit.

**Important:**
- Do NOT use `git add -A` or `git add .` — stage specific files by name.
- Do NOT include files that may contain secrets (`.env`, credentials, tokens, etc.).
- If there are multiple logical units of change, suggest splitting into separate commits.

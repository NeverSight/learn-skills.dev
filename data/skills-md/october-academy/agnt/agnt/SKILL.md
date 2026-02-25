---
name: agnt
description: Guides users through Agentic30's MUD-style 30-day learning journey. Use when the user asks to start, continue, submit, reset, or check status for Agentic30 quests, onboarding, interview-driven development, or landing deployment.
license: MIT
compatibility: Designed for filesystem-based coding agents (Codex, Claude Code) with optional MCP access to https://mcp.agentic30.app/mcp.
metadata:
  author: october-academy
  version: "1.0.0"
---

# agnt

Agentic30 학습 여정을 안내하는 공용 Agent Skill입니다.

## When To Use

다음 요청에서 이 스킬을 사용합니다.

- "agnt 시작", "day 0부터 시작", "학습 이어하기"
- "오늘 퀘스트 보여줘", "진행 상태 확인"
- "퀘스트 제출", "초기화"
- "Agentic30 인터뷰 기반으로 진행"
- Codex 명시형 호출: `$agnt-continue`, `$agnt-init`, `$agnt-today`, `$agnt-submit`, `$agnt-status`

## Runtime Setup

### 0) 에이전트 환경 분기

실행 환경을 먼저 확인합니다.

- Claude Code 환경: `/mcp` 명령이 사용 가능하거나 사용자가 Claude Code를 사용 중임
- Codex 환경: `codex` CLI 사용 중임

이후 MCP 연결 절차를 환경별로 따릅니다.

### 1) MCP 연결 확인 (환경별)

#### A. Claude Code

`agentic30` MCP 서버가 없으면 아래 순서로 안내합니다.

1. Claude Code 실행
2. 채팅 입력창에 `/mcp` 입력
3. 목록에서 `agentic30` 또는 `plugin:agnt:agentic30` 선택
4. `Authenticate` 선택 후 브라우저에서 Google 로그인
5. `/mcp`에서 connected 상태 확인

서버가 목록에 없으면 프로젝트 `.mcp.json`에 아래 항목을 추가합니다.

```json
{
  "mcpServers": {
    "agentic30": {
      "type": "http",
      "url": "https://mcp.agentic30.app/mcp"
    }
  }
}
```

그 뒤 Claude Code를 재시작하고 `/mcp` 인증을 다시 진행합니다.

#### B. Codex

`agentic30` MCP 서버가 없으면 아래 순서로 안내합니다.

```bash
codex mcp add agentic30 --url https://mcp.agentic30.app/mcp
codex mcp login agentic30
codex mcp list
```

이미 등록되어 있으면 `codex mcp login agentic30`만 다시 수행하면 됩니다.

### 2) 상태 파일 경로(AGNT_DIR)

아래 순서로 state 경로를 탐색합니다.

1. `.claude/agnt/state.json`
2. `~/.claude/agnt/state.json`
3. `.codex/agnt/state.json`
4. `~/.codex/agnt/state.json`
5. 둘 다 없으면 `.claude/agnt/state.json` 생성

### 3) references 경로(REFS_DIR)

아래 순서로 references 경로를 탐색합니다.

1. `references/` (현재 스킬 디렉토리 기준)
2. `{AGNT_DIR}/references`
3. `~/.claude/plugins/marketplaces/agentic30/references`
4. `.agents/skills/agnt/references`
5. `~/.codex/skills/agnt/references`

## Command Mapping

사용자 의도를 아래 파일로 매핑해 실행합니다.

- 이어하기: `commands/continue.md`
- 초기화: `commands/init.md`
- 오늘 퀘스트: `commands/today.md`
- 제출: `commands/submit.md`
- 상태: `commands/status.md`

각 파일의 절차/규칙을 source of truth로 사용합니다.

### Codex Command Style (`$agnt-*`)

Codex에서는 아래 명령을 canonical로 사용합니다.

- `$agnt-continue` → `commands/continue.md`
- `$agnt-init` → `commands/init.md`
- `$agnt-today` → `commands/today.md`
- `$agnt-submit` → `commands/submit.md`
- `$agnt-status` → `commands/status.md`

호환 입력(`$agnt continue`, `$agnt init` 등)도 동일하게 매핑합니다.

## Agent Compatibility Rules

`commands/*.md`는 Claude Plugin 기준 문구(`ToolSearch`, `AskUserQuestion`, `/mcp`)를 포함합니다.
Codex 등 다른 에이전트에서는 아래로 호환 처리합니다.

- `ToolSearch`:
  - 가능하면 MCP 도구 목록/호출로 `agentic30` 연결 여부를 확인합니다.
  - 확인 불가 시, `submit_practice` 또는 `get_leaderboard` 호출을 시도하고 실패를 연결 실패로 처리합니다.
- `AskUserQuestion`:
  - 일반 질문으로 대체하되, 선택지를 번호 목록으로 명시합니다.
- `/mcp` 안내:
  - Claude Code에서는 `/mcp` 안내를 그대로 사용합니다.
  - Codex에서는 `codex mcp add/login/list` 명령으로 치환합니다.
- 경로 안내:
  - Codex에서 `commands/*.md`를 읽을 때 `.claude/agnt` 경로 표기가 나오면 `.codex/agnt`를 우선 사용합니다.
- 명령 파싱 우선순위:
  1. `$agnt-<subcommand>` canonical 입력
  2. `$agnt <subcommand>` 호환 입력
  3. 자연어 의도 입력 (예: "오늘 퀘스트 보여줘")

## Core Behavior Rules

- 한국어로 진행하고 기술 용어는 원문(MCP, OAuth, CLI) 유지
- `references/shared/narrative-engine.md`의 STOP PROTOCOL 준수
- 블록/퀘스트 판정은 각 Day의 `index.json` 우선
- MCP 연결 실패 시 fail-closed (완료 제출/동기화 금지)
- Day 1 `block3-deploy`는 `deploy_landing` MCP 경로를 우선 사용
